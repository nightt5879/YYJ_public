/*
for timer
*/
#include <REGX52.H>

void Timer0Init(void)		//11.0592MHz
{
	//AUXR &= 0x7F;		
	TMOD &= 0xF0;		
	TMOD |= 0x01;		
	TL0 = 0x66;		
	TH0 = 0xFC;		
	TF0 = 0;		
	TR0 = 1;
	//Below is start work
	ET0 = 1;
	EA = 1;
	//PT0 = 0;	
}

void Timer1Init(void)		//11.0592MHz
{
	//AUXR &= 0xBF;		
	TMOD &= 0x0F;		
	TMOD |= 0x10;		
	TL1 = 0x66;		
	TH1 = 0xFC;		
	TF1 = 0;		
	TR1 = 1;	
	//Below is start work
	ET1 = 1;
	EA = 1;
	//PT1 = 1;
}

void Timer2Init(void)		//@11.0592MHz
{
	T2MOD = 0;	
	T2CON = 0;	
	TL2 = 0x66;	
	TH2 = 0xFC;	
	RCAP2L = 0x66;	
	RCAP2H = 0xFC;	
	TR2 = 1;	
	//Below is start work
	ET2 = 1;
	EA = 1;
	//PT1 = 1;	
}

/*
void Timer0_Routine() interrupt 1
{
	static unsigned int T0Count;
	TL0 = 0x66;		
	TH0 = 0xFC;	
	T0Count++;
	if(T0Count >= 50)//50ms
	{
		P2_0 = ~P2_0;
		T0Count=0;
	}
}
*/


/*
void Timer0_Init()
{
	//TMOD = 0x01;
	TMOD &= 0xF0; //only change the lower 4 places
	TMOD |= TMOD|0x01; //change the last digit
	TF0 = 0;
	TR0 = 1;
	//frequency = 11.059MHz
	TH0 = 64448/256;
	TL0 = 64448%256;  //Assign to two 8-bit registers
	/*
	Similar to: 123 to 1 and 23 two boxs
	(each box can only hold 0 to 99)
	here is the 16-bit register, so using the 2^8 = 256
	//
	ET0 = 1;
	EA = 1;
	PT0 = 0;
}
*/
