#!/usr/bin/env python3

import asyncio
import moteus

async def main():
    controller = moteus.Controller(id=1)
    
    await controller.set_stop()
    await asyncio.sleep(0.5)
    
    # Try with different parameters
    print("Attempting position command with higher limits...")
    result = await controller.set_position(
        position=1.0,
        velocity=0,
        maximum_torque=2.0,      # Higher torque limit
        velocity_limit=5.0,       # Higher velocity limit  
        accel_limit=2.0,          # Higher accel limit
        query=True
    )
    
    print(f"Initial Result: {result}")
    
    # Monitor for 5 seconds (50 iterations at 0.1s)
    for i in range(50):
        result = await controller.query()
        pos = result.values.get(moteus.Register.POSITION, None)
        q_current = result.values.get(moteus.Register.Q_CURRENT, None)

        pos_str = f"{pos:.3f}" if pos is not None else "N/A"
        q_str = f"{q_current:.3f}" if q_current is not None else "N/A"

        print(f"pos={pos_str}, q_A={q_str}")
        await asyncio.sleep(0.1)
    
    await controller.set_stop()

asyncio.run(main())
