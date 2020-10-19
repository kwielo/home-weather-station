
print('hi!')

send_data = function()
  http.get("http://192.168.10.53:8000/api/collect", nil, function (code, data)
    if code < 0 then
      print("http request failed")
    else
      print("http request successful: "..data)
    end
  end)
  tmr.create():alarm(5000, tmr.ALARM_SINGLE, send_data)
end

send_data()

while true do
  tmr.create():alarm(5000, tmr.ALARM_SINGLE, send_data)
end