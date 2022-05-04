
#include "battery.h"
#include "esp_camera.h"
#include "camera_pins.h"
#include "network.h"
//#include "bmm8563.h"
//#include "led.h"

Network network;
String networkName = "YourSSID";
String networkPswd = "YourPW";
String networkAddress = "192.168.your.PCIP";
int networkPort = 3333;

//const int pinButton = 37;
//const int pinLED = 37;

void setup() {
  Serial.begin(115200);
  bat_init();
  //bmm8563_init();
  //led_init(CAMERA_LED_GPIO);
  Serial.setDebugOutput(true);
  Serial.println();
  //LED BTN
  //pinMode(pinButton, INPUT_PULLUP);
  //pinMode(pinLED, OUTPUT);
  //digitalWrite(pinLED, HIGH);

  //Camera
  camera_config_t camera_config;
  camera_config.ledc_channel = LEDC_CHANNEL_0;
  camera_config.ledc_timer = LEDC_TIMER_0;
  camera_config.pin_d0 = Y2_GPIO_NUM;
  camera_config.pin_d1 = Y3_GPIO_NUM;
  camera_config.pin_d2 = Y4_GPIO_NUM;
  camera_config.pin_d3 = Y5_GPIO_NUM;
  camera_config.pin_d4 = Y6_GPIO_NUM;
  camera_config.pin_d5 = Y7_GPIO_NUM;
  camera_config.pin_d6 = Y8_GPIO_NUM;
  camera_config.pin_d7 = Y9_GPIO_NUM;
  camera_config.pin_xclk = XCLK_GPIO_NUM;
  camera_config.pin_pclk = PCLK_GPIO_NUM;
  camera_config.pin_vsync = VSYNC_GPIO_NUM;
  camera_config.pin_href = HREF_GPIO_NUM;
  camera_config.pin_sscb_sda = SIOD_GPIO_NUM;
  camera_config.pin_sscb_scl = SIOC_GPIO_NUM;
  camera_config.pin_pwdn = PWDN_GPIO_NUM;
  camera_config.pin_reset = RESET_GPIO_NUM;
  camera_config.xclk_freq_hz = 20000000;
  camera_config.pixel_format = PIXFORMAT_JPEG;
  camera_config.frame_size = FRAMESIZE_240X240;
  camera_config.jpeg_quality = 10;
  camera_config.fb_count = 2;
  esp_err_t err = esp_camera_init(&camera_config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }
  sensor_t * s = esp_camera_sensor_get();
  s->set_vflip(s, 1);//flip it back
  s->set_brightness(s, 1);//up the blightness just a bit
  s->set_saturation(s, -2);//lower the saturation

  //Network
  network.begin(networkName, networkPswd);
}

void loop() {
  //PinDeepSleep
  //if(digitalRead(pinButton) == HIGH){
  //  Serial.println("Sleep...");
  //  digitalWrite(pinLED, LOW);
  //  esp_sleep_enable_ext0_wakeup(GPIO_NUM_37, HIGH);
  //  esp_deep_sleep_start();
  //}
  //Camera
  camera_fb_t * fb = NULL;
  fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }
  Serial.print("size:");
  Serial.println(fb->len);
  network.send(fb->buf, fb->len, networkAddress, networkPort);
  esp_camera_fb_return(fb);
}
