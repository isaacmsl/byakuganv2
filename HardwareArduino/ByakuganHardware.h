class ByakuganHardware : public ArduinoHardware
{
  public:
  ByakuganHardware():ArduinoHardware(&Serial3, 115200){};
};
