#ifndef INC_LSM6DSLX_H_
#define INC_LSM6DSLX_H_

#include "lsm6dsl.h"
#include "b_l4s5i_iot01a_bus.h"

LSM6DSL_Object_t MotionSensor;

static void MEMS_Init(void) {
	LSM6DSL_IO_t io_ctx;
	uint8_t id;
	LSM6DSL_AxesRaw_t axes;

	/* Link I2C functions to the LSM6DSL driver */
	io_ctx.BusType = LSM6DSL_I2C_BUS;
	io_ctx.Address = LSM6DSL_I2C_ADD_L;
	io_ctx.Init = BSP_I2C2_Init;
	io_ctx.DeInit = BSP_I2C2_DeInit;
	io_ctx.ReadReg = BSP_I2C2_ReadReg;
	io_ctx.WriteReg = BSP_I2C2_WriteReg;
	io_ctx.GetTick = BSP_GetTick;
	LSM6DSL_RegisterBusIO(&MotionSensor, &io_ctx);

	/* Read the LSM6DSL WHO_AM_I register */
	LSM6DSL_ReadID(&MotionSensor, &id);
	if (id != LSM6DSL_ID) {
		Error_Handler();
	}

	/* Initialize the LSM6DSL sensor */
	LSM6DSL_Init(&MotionSensor);

	/* Configure the LSM6DSL accelerometer (ODR, scale and interrupt) */
	LSM6DSL_ACC_SetOutputDataRate(&MotionSensor, 26.0f); /* 26 Hz */
	LSM6DSL_ACC_SetFullScale(&MotionSensor, 4); /* [-4000mg; +4000mg] */
	LSM6DSL_ACC_Set_INT1_DRDY(&MotionSensor, ENABLE); /* Enable DRDY */
	LSM6DSL_ACC_GetAxesRaw(&MotionSensor, &axes); /* Clear DRDY */

	/* Start the LSM6DSL accelerometer */
	LSM6DSL_ACC_Enable(&MotionSensor);
}

#endif
