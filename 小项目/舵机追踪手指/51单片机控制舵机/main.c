#include <REGX52.H>
#include "Delay.h"
#include "UART.h"

//on the bottom is logic level
sbit IN1 = P2^0;
sbit IN2 = P2^1;
sbit IN3 = P2^2;
sbit IN4 = P2^3;
//on the bottom is PWM
sbit PWM1=P2^4;
sbit PWM2=P2^5;
int time;
int x,y;
int Xmax,Xmin,Ymax,Ymin;
//on the bottom is infrared
sbit Input_l = P2^6;
sbit Input_r = P2^7;

void Delay1ms()		//@11.0592MHz
{
	unsigned char i, j;

	//_nop_();
	i = 2;
	j = 199;
	do
	{
		while (--j);
	} while (--i);
}




void main()
{
	UART_Init();		//串口初始化
	//defining timers
	//TMOD=0x01;
	TH0=0xff;
	TL0=0xf7;
	EA=1;
	ET0=1;
	TR0=1;
	IN1 = 0;
	//init engine
	x = 21;
	y =6;
	Xmax = 37;
	Xmin = 6;
	Ymax = 20;
	Ymin = 6;
	time = 0;
	while(1)
	{
		if(RI==1)					//如果接收标志位为1，接收到了数据
		{			
			//UART_SendByte(SBUF);		
			if(SBUF == 0xE1){
				if(x>Xmin)x--;
				if(y<Ymax) y++;
				UART_SendByte(SBUF);
			}
			else if(SBUF == 0xE2){
				x=x;
				if(y<Ymax)y++;
			}
			else if(SBUF == 0xE3){
				if(x<Xmax)x++;
				if(y<Ymax)y++;
			}
			else if(SBUF == 0xE4){
				if(x>Xmin)x--;
				y=y;
			}
			else if(SBUF == 0xE5){
				x=x;
				y=y;
			}
			else if(SBUF == 0xE6){
				if(x<Xmax)x++;
				y=y;
			}
			else if(SBUF == 0xE7){
				if(x>Xmin)x--;
				if(y>Ymin)y--;
			}
			else if(SBUF == 0xE8){
				x=x;
				if(y>Ymin)y--;
			}
			else if(SBUF == 0xE9){
				if(x<Xmax)x++;
				if(y>Ymin)y--;
			}
			RI=0;					//接收标志位清0
	}
		
	}
}
/*
void UART_Routine() interrupt 4 
{
	if(RI==1)					//如果接收标志位为1，接收到了数据
	{			
		//UART_SendByte(SBUF);		
		if(SBUF == 0xE1){
			if(x<37)x++;
			if(y<20) y++;
			UART_SendByte(SBUF);
		}
		else if(SBUF == 0xE2){
			x=x;
			if(y<20)y++;
		}
		else if(SBUF == 0xE3){
			if(x>6)x--;
			if(y<20)y++;
		}
		else if(SBUF == 0xE4){
			if(x<37)x--;
			y=y;
		}
		else if(SBUF == 0xE5){
			x=x;
			y=y;
		}
		else if(SBUF == 0xE6){
			if(x>6)x--;
			y=y;
		}
		else if(SBUF == 0xE7){
			if(x<37)x++;
			if(y>6)y--;
		}
		else if(SBUF == 0xE8){
			x=x;
			if(y>6)y--;
		}
		else if(SBUF == 0xE9){
			if(x>6)x--;
			if(y>6)y--;
		}
		RI=0;					//接收标志位清0
	}
}
*/


//time interrupt for PWM
void tim0() interrupt 1
{
	TR0=0;	
	TH0=0xff;	
	TL0=0xf7;	//0.01ms
	TR0=1;		
	time++;
	if(time>=300) time=0;	//you can change time to change PWM
	if(time<=x) PWM1= 1;		//20 is to 1ms
	else PWM1 = 0;
	if(time<=y) PWM2 = 1;
	else PWM2 = 0;
}



