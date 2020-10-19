import web

db = web.database(
    dbn='postgres',
    host='192.168.10.53',
    port=5432,
    user='dev',
    pw='d3v',
    db='weather_station',
)
urls = (
    '/', 'Index',
    '/history/(\d+)', 'Measures',
    '/api/collect', 'Collect'
)


class MeterRepo:
    def all():
        return db.select("meter")


render = web.template.render('tpl/', base='base', globals={'MeterRepo': MeterRepo, 'ctx': web.ctx})


class Index:
    def GET(self):
        measures = []
        for meter in MeterRepo.all():
            measures.append(
                db.query("""
                    select
                        measure.*,
                        meter.name as meter_name,
                        meter.location as meter_location,
                        to_char(measure.measured_at at time zone 'Europe/Warsaw', 'DD Mon YYYY, HH24:MI:SS') as measured_at,
                        (
                            select round(avg(avg_m.temperature), 2) as avg_temp
                            from measure avg_m
                            where avg_m.meter_id = $meter_id
                              and avg_m.measured_at > (now() - interval '24 hours')
                            group by avg_m.meter_id
                        ),
                        round(pressure+(121/(8000*((1+0.004*temperature)/pressure))), 2) as mslp
                    from measure
                        join meter on meter.id = measure.meter_id
                    where measure.meter_id = $meter_id
                    order by measure.measured_at desc
                    limit 1
                """, vars=dict(meter_id=meter.id))[0]
            )

        return render.index(measures=measures)


class Measures:
    def GET(self, id):
        measures = db.query("""
                select 
                    measure.*,
                    meter.name as meter_name,
                    meter.location as meter_location,
                    to_char(measure.measured_at at time zone 'Europe/Warsaw', 'DD Mon YYYY, HH24:MI:SS') as measured_at
                from measure
                    join meter on meter.id = measure.meter_id 
                where measure.meter_id = $meter_id 
                order by measure.measured_at desc
                limit 30
            """, vars=dict({'meter_id': id}))

        return render.measures(measures=measures, id=id)


class Collect:
    def GET(self):
        return '{"message":"go it!"}'


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()


