#include "network.h"

#include <WiFi.h>
#include <WiFiUdp.h>

WiFiUDP udp;
String _ssid;
String _pwd;

byte id = 0;
const int frag = 1024;

void Network::begin(String ssid, String pwd) {
  _ssid = ssid;
  _pwd = pwd;
  WiFi.disconnect(true);
  WiFi.begin(ssid.c_str(), pwd.c_str());
  while ( WiFi.status() != WL_CONNECTED)delay(500);
}
void Network::send(byte* data, const int size, String address, const int port) {
  if (WiFi.status() == WL_CONNECTED) {
    int num = 0;
    for (int i = 0; i < size; i+= frag) {
      udp.beginPacket(address.c_str(), port);
      udp.write(id);
      udp.write(size % 256);
      udp.write(size / 256);
      udp.write(num);
      udp.write(data + i, min(frag, size - i));
      udp.endPacket();
      num++;
    }
    if (id == 255)id = 0;
    else id++;
  }
  else {
    begin(_ssid, _pwd);
  }
}
