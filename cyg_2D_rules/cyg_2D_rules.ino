#include<SoftwareSerial.h>
//#include<print.h>

#define LED_NUM 13

// 모터 PIN 번호 설정

// #define PIN_L_Motor_PWM 6 // Motor(L) PWM

// #define PIN_L_Motor_DIR 7 // Motor(L) Directory

// #define PIN_R_Motor_PWM 5 // Motor(R) PWM

// #define PIN_R_Motor_DIR 4 // Motor(R) Directory

#define PACKET_ALL (5+323+1) //HEADER3 + LENGTH2 + PAYLOAD + CHECKSUM​

SoftwareSerial CygLiDAR(19, 18);

// LIDAR Data Receive

byte packetbuffer[PACKET_ALL] = {0};

byte checksum = 0;

bool togglebuffer = true;

volatile bool finish_buf = false;

int buffCnt = 0;

int state = 0;

int CLcount = 0;

unsigned int distanceA[161] = {0};

unsigned int distanceB[161] = {0};

unsigned int *distance;


byte Start_LiDAR[8] = {0x5A, 0x77, 0xFF, 0x02, 0x00, 0x01, 0x00, 0x03};

byte Stop_LiDAR[8] = {0x5A, 0x77, 0xFF, 0x02, 0x00, 0x02, 0x00, 0x00};

// int PWM_L;

// int PWM_R;


// Motor ( R & L ), pwm > 0 : forward, pwm < 0 : backward

// void MotorL(int pwm) {

//   if (pwm > 0) {

//     analogWrite(PIN_L_Motor_PWM, pwm);

//     digitalWrite(PIN_L_Motor_DIR, LOW);

//   }

//   else {

//     analogWrite(PIN_L_Motor_PWM, -1 * (pwm));

//     digitalWrite(PIN_L_Motor_DIR, HIGH);

//   }

// }

// void MotorR(int pwm) {

//   if (pwm > 0) {

//     analogWrite(PIN_R_Motor_PWM, pwm);

//     digitalWrite(PIN_R_Motor_DIR, HIGH);

//   }

//   else {

//     analogWrite(PIN_R_Motor_PWM, -1 * (pwm));

//     digitalWrite(PIN_R_Motor_DIR, LOW);

//   }

// }

void setup() {

  // put your setup code here, to run once:

 
  pinMode(LED_NUM, OUTPUT);

//   car_stop();



  CygLiDAR.begin(57600);



  Serial.begin(115200);

  //Serial.begin(57600);

  Serial.available();



  //Start LiDAR

  CygLiDAR.write(Start_LiDAR[0]);

  CygLiDAR.write(Start_LiDAR[1]);

  CygLiDAR.write(Start_LiDAR[2]);

  CygLiDAR.write(Start_LiDAR[3]);

  CygLiDAR.write(Start_LiDAR[4]);

  CygLiDAR.write(Start_LiDAR[5]);

  CygLiDAR.write(Start_LiDAR[6]);

  CygLiDAR.write(Start_LiDAR[7]);

  CygLiDAR.available();

  delay(500);



}

// void car_go()

// {

//   MotorL(200); //debug

//   MotorR(200); //debug

// }

// void car_back()

// {

//   MotorL(-200); //debug

//   MotorR(-200); //debug

// }

// void car_right()

// {

//   MotorL(0); //debug

//   MotorR(200); //debug

//   // delay(100);

// }

// void car_left()

// {

//   MotorL(200); //debug

//   MotorR(0); //debug

//   // delay(100);

// }

// void car_turn()

// {

//   MotorL(-200); //debug

//   MotorR(200); //debug

//   // delay(100);



// }

// void car_stop()

// {

//   MotorL(0); //debug

//   MotorR(0); //debug



// }

//0: stop , 1:go ,2:right , 3:left ,4:turn

int DetectEnv()

{

  int state = 0;

  int stopp = 0;

  if ( (togglebuffer == true)) distance = distanceA;

  else distance = distanceB;



  for(int i =0 ; i<160;i++){
    if(distance[i] <600 ) stopp++;
  }


  if (stopp < 50) state = 1;

  else state = 2;

  return state;

}


//완료된 배열에서 거리 값 만들기

void loop() {

  CygSerialEvent();



  if (finish_buf == true)

  {

    //for (int i=0 ; i<161 ; i++){
      //  Serial.print(distance[i]);
      //  Serial.print(" ");
      //  }
    //Serial.println("");
    
    //while(1);
    finish_buf = false;



    switch (DetectEnv())

    {

      case 0: //Serial.println("stop");
        Serial.write("w");

        break;

      case 1: 
        Serial.write("g");
        break;

      case 2: 
        Serial.write("s");
        break;
        
    }



  }

  


}






int packet_cnt;
void CygSerialEvent()

{

  while (finish_buf == false)

  {

    int bufSize;

    

    bufSize = CygLiDAR.readBytes(packetbuffer, PACKET_ALL);
    //Serial.print(bufSize);
    //Serial.print(" ");
    //if(packet_cnt++ % 16 == 0)
    //   Serial.println(" ");
    
    
      
      for (int i = 0; i < bufSize; i++)

    {

      if (state == 0)

      {

        

        buffCnt = 0;

        if (packetbuffer[i] == 0x5A)

        {

          state = 1;

        }

      }

      else if (state == 1)

      {

        if (packetbuffer[i] == 0x77)

        {

          state = 2;

        }

        else

        {

          state = 0;

        }

      }

      else if (state == 2)

      {

        if (packetbuffer[i] == 0xFF)

        {

          state = 3;

        }

        else

        {

          state = 0;

        }

      }

      else if (state == 3)

      {

        if (packetbuffer[i] == 0x43)

        {

          checksum = 0;

          state = 4;

          checksum ^= packetbuffer[i];

        }

        else

        {

          state = 0;

        }

      }

      else if (state == 4)

      {

        if (packetbuffer[i] == 0x01)

        {

          state = 5;

          checksum ^= packetbuffer[i];

        }

        else

        {

          state = 0;

        }

      }

      else if (state == 5)

      {

        if (packetbuffer[i] == 0x01)

        {

          if (togglebuffer == true) togglebuffer = false;

          else togglebuffer = true;

          checksum ^= packetbuffer[i];

          state = 6;

          CLcount = 0;

        }

        else

        {

          state = 0;

        }

      }

      else if (state == 6) //scan

      {

        checksum ^= packetbuffer[i];

        

        if (togglebuffer == true)

        {

          if (CLcount % 2 == 0) distanceA[CLcount / 2] = ((packetbuffer[i] << 8) & 0xff00);

          else distanceA[CLcount / 2] |= (unsigned int)packetbuffer[i] ;

        } else

        {

          if (CLcount % 2 == 0) distanceB[CLcount / 2] = ((packetbuffer[i] << 8) & 0xff00);

          else distanceB[CLcount / 2] |= (unsigned int)packetbuffer[i] ;

          

        }

        CLcount++;

        if (CLcount >= 322) {

          state = 7;

          

        }


        
      }

      else if (state == 7) //checksum

      {

        CLcount = 0;

        state = 0;

        if (checksum == packetbuffer[i]) {

          finish_buf = true;
          

          digitalWrite(LED_NUM, HIGH);

        
       

        }

        else {

          digitalWrite(LED_NUM, LOW);

        }

        checksum = 0;

      }

      else

      {

        state = 0;

      }

    }

    

  }

}
