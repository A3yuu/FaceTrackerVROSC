#include "Arduino.h"

class Network {
  public:
    void begin(String ssid, String pwd);
    void send(byte* data, const int size, String address, const int port);
};
