import asyncio
import moteus

async def set_pid_values():
    controller = moteus.Controller(id=1)
    
    # Stop the controller first
    await controller.set_stop()
    await asyncio.sleep(0.1)
    
    # Write config values
    await controller.write_config({
        'servo.pid_position.kp': 0.1,
        'servo.pid_position.kd': 0.01,
        'servo.pid_position.ki': 0.0,
    })
    
    print("PID values written!")
    
    # Read back to verify
    config = await controller.read_config([
        'servo.pid_position.kp',
        'servo.pid_position.kd', 
        'servo.pid_position.ki'
    ])
    
    print(f"Verified values:")
    for key, value in config.items():
        print(f"  {key}: {value}")

if __name__ == '__main__':
    asyncio.run(set_pid_values())