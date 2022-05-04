#include <REGX52.H>
#include "Delay.h"
#include "UART.h"
#include "Timer.h"


//on the bottom is logic level
sbit IN1 = P2^3;
sbit IN2 = P2^2;
sbit IN3 = P2^1;
sbit IN4 = P2^0;
//on the bottom is PWM
sbit PWM1=P2^4;
sbit PWM2=P2^5;
int time;
//on the bottom is infrared
sbit Input_l = P2^6;
sbit Input_r = P2^7;
//on the bottom is duty cycle
int L_PWM,R_PWM;


/*
agreement:
N1&N2:left two wheels
N3&N4:right two wheels
+-:forward
-+:back
--&++:stop
*/

void main()
{
	UART_Init();
	Timer0Init();
	Timer2Init();
	L_PWM = R_PWM = 5;
	IN1=IN2=IN3=IN4=0;  //stop
	while(1)
	{
		
	}
}

void UART_Routine() interrupt 4
{
	if(RI==1)					
	{	
		UART_SendByte(SBUF);
		if(SBUF == 0x00)  //stop
		{
			IN1=IN2=IN3=IN4=0;
		}
		if(SBUF == 0x01)  //forward
		{
			IN1=IN3=1;
			IN2=IN4=0;
		}
		if(SBUF == 0x02) //back
		{
			IN1=IN3=0;
			IN2=IN4=1;
		}
		if(SBUF == 0x03) //turn_left
		{
			IN1=IN4=0;
			IN2=IN3=1;
		}
		if(SBUF == 0x04) //turn_right
		{
			IN1=IN4=1;
			IN2=IN3=0;
		}
		if(SBUF == 0x05) //speed up
		{
			if(L_PWM <= 20)
			{
				L_PWM++;
				R_PWM++;
			}
		}
		if(SBUF == 0x06) //speed dowm
		{
			if(L_PWM >= 1)
			{
				L_PWM--;
				R_PWM--;
			}
		}
		if(SBUF == 0x07) //reset
		{
			L_PWM = R_PWM = 5;
		}
		if(SBUF == 0x08) //full_speed
		{
			L_PWM = R_PWM = 20;
		}
	RI=0;					
	}
}

void Timer0_Routine() interrupt 1  //for left_wheel
{
	static unsigned int T0Count;
	TL0 = 0x66;		
	TH0 = 0xFC;	 //1ms
	T0Count++;
	if(T0Count >= 20) T0Count = 0;
	if(T0Count <= L_PWM) PWM1 = 1;
	else PWM1 = 0;
}

void Timer2_Routine() interrupt 5  //for right_wheel
{
	static unsigned int T2Count;
	TF2 = 0;  //1ms
	T2Count++;
	if(T2Count >= 20) T2Count = 0;
	if(T2Count <= R_PWM) PWM2 = 1;
	else PWM2 = 0;
}

