#!/usr/bin/env python3
"""
Motor Position Control Script for Moteus Controller
Based on your setup with MAD-5005 motor on Raspberry Pi
"""

import asyncio
import moteus
import time

async def main():
    # Create a moteus controller instance
    # If your motor is on a different ID than 1, change it here
    controller = moteus.Controller(id=1)
    
    # Create a stream object for sending commands
    stream = moteus.Stream(controller)
    
    print("Starting motor position control...")
    print("Press Ctrl+C to stop")
    
    try:

        state = await c.set_position(position=math.nan, query=True)
        
        # Example 1: Move to a specific position
        print("\nMoving to position 0.5 revolutions...")
        # await controller.set_position(
        #     position=0.5,  # Target position in revolutions
        #     # velocity=0.2,  # Max velocity
        #     # accel_limit=0.2,  # Acceleration limit
        #     query=True  # Request status feedback
        # )

        await controller.set_position(
            position=0.5,
            velocity=0.0,
            accel_limit=8.0,
            velocity_limit=3.0,
            query=True,
        )

        await asyncio.sleep(3)  # Wait for movement to complete
        
        # Example 2: Move to another position
        print("Moving to position -0.2 revolutions...")
        # await controller.set_position(
        #     position=-0.2,
        #     # velocity=0.2,
        #     # accel_limit=0.2,
        #     query=True
        # )

        await controller.set_position(
            position=-0.2,
            velocity=0.0,
            accel_limit=8.0,
            velocity_limit=3.0,
            query=True,
        )

        await asyncio.sleep(3)
        
        # Example 3: Get current status
        print("\nQuerying motor status...")
        result = await controller.query()
        print(f"Current position: {result.values[moteus.Register.POSITION]:.3f} rev")
        print(f"Current velocity: {result.values[moteus.Register.VELOCITY]:.3f} rev/s")
        print(f"Motor temperature: {result.values[moteus.Register.TEMPERATURE]:.1f}°C")
        
        # Example 4: Move through a sequence of positions
        print("\nRunning position sequence...")
        positions = [0.0, 0.25, 0.5, 0.25, 0.0, -0.25, -0.5, -0.25, 0.0]
        
        for pos in positions:
            print(f"Moving to position: {pos}")
            await controller.set_position(
                position=pos,
                velocity_limit=0.3,
                accel_limit=0.3,
                query=True
            )
            await asyncio.sleep(1.5)
        
        # Stop the motor
        print("\nStopping motor...")
        await controller.set_stop()
        
    except KeyboardInterrupt:
        print("\nStopping motor due to keyboard interrupt...")
        await controller.set_stop()
    
    except Exception as e:
        print(f"Error occurred: {e}")
        await controller.set_stop()
    
    finally:
        print("Script completed")

if __name__ == "__main__":
    asyncio.run(main())