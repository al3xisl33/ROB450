import asyncio
import moteus
import math

"""
want to test 
1. set_position(position, accel_limit)
2. set_position(position=nan, velocity_limit=0.5, accel_limit=2.0)
i want to figure out why set_position only works sometimes and why set_position_and_wait works 

"""

async def main():
    # Construct a default controller at id 1.
    c = moteus.Controller(id=1)

    # Clear any outstanding faults.
    await c.set_stop()
    await c.set_position(0)

    while True:
        # This will periodically command and poll the controller until
        # the target position achieves the commanded value.
        result = await c.set_position_wait_complete(
            position=0.5, velocity_limit=3.0, accel_limit=2.0)
        # print(result)

        print("\nQuerying motor status...")
        result = await c.query()
        print(f"Current position: {result.values[moteus.Register.POSITION]:.3f} rev")
        print(f"Current velocity: {result.values[moteus.Register.VELOCITY]:.3f} rev/s")
        print(f"Motor temperature: {result.values[moteus.Register.TEMPERATURE]:.1f}°C")

        # Then go back to zero, and eventually try again.
        result = await c.set_position_wait_complete(
            position=0.0, accel_limit=2.0)
        # print(result)

        print("\nQuerying motor status...")
        result = await c.query()
        print(f"Current position: {result.values[moteus.Register.POSITION]:.3f} rev")
        print(f"Current velocity: {result.values[moteus.Register.VELOCITY]:.3f} rev/s")
        print(f"Motor temperature: {result.values[moteus.Register.TEMPERATURE]:.1f}°C")


if __name__ == '__main__':
    asyncio.run(main())
