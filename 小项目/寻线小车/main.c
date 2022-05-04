/*******************************************************************/
/*
car_control 
yyj 
22/4/5
*/
/*****************************************************************/

#include<reg52.h>
#define uint unsigned int
#define uchar unsigned char


//on the bottom is logic level
sbit IN1 = P2^0;
sbit IN2 = P2^1;
sbit IN3 = P2^2;
sbit IN4 = P2^3;
//on the bottom is PWM
sbit PWM1=P2^4;
sbit PWM2=P2^5;
int time;
//on the bottom is infrared
sbit Input_l = P2^6;
sbit Input_r = P2^7;


/*
agreement:
N1&N2:left two wheels
N3&N4:right two wheels
+-:back
-+:forward
--&++:stop
*/

void main()
{
	//defining timers
	TMOD=0x01;
	TH0=0xff;
	TL0=0xf7;
	EA=1;
	ET0=1;
	TR0=1;
	
	IN1=IN3 = 1;
	IN2=IN4 = 0;
	//PWM1=PWM2 = 1;
	while(1)
	{
		if(Input_r&&Input_l)  //forward
		{
			IN1=IN3=0;
			IN2=IN4=1;
		}
		else if(Input_r&&(~Input_l))  //turn left
		{
			IN1=IN4=IN3=0;
			IN2=1;
		}
		else if((~Input_r)&&Input_l)  //turn right
		{
			IN1=IN2=IN3=0;
			IN4=1;
		}
		else  //stop
		{
			IN1=IN2=IN3=IN4=0;
		}
	}
}

 


//time interrupt for PWM
void tim0() interrupt 1
{
       TR0=0;	
       TH0=0xff;	
       TL0=0xf7;	//0.01ms
       TR0=1;		
       time++;
       if(time>=100) time=0;	//you can change time to change PWM
       if(time<=20) PWM1=PWM2 = 1;		//20 is to 1ms
       else PWM1=PWM2 =0;
}
