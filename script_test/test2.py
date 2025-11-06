#!/usr/bin/env python3

import asyncio
import moteus

async def main():
    # Create a moteus controller instance (ID 1 by default)
    controller = moteus.Controller()
    
    # Example 1: Position control
    await controller.set_position(
        position=2.0,      # position in revolutions
        velocity=0.0,      # velocity in rev/s (optional)
        maximum_torque=0.3, # max torque in Nm
        velocity_limit=0.2, # max velocity
        accel_limit=0.2     # max acceleration
    )
    
    # Wait for 2 seconds
    await asyncio.sleep(2.0)
    
    # Example 2: Torque control (using d/q currents)
    await controller.set_current(
        d_A=0.0,  # d-axis current
        q_A=2.0   # q-axis current (produces torque)
    )
    
    await asyncio.sleep(2.0)
    
    # Example 3: Stop the motor
    await controller.set_stop()

# Run the async main function
asyncio.run(main())