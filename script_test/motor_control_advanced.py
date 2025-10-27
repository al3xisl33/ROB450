#!/usr/bin/env python3
"""
Advanced Motor Control Script with Real-time Monitoring
Supports position, velocity, and torque control modes
"""

import asyncio
import moteus
import time
import math

class MotorController:
    def __init__(self, motor_id=1):
        self.controller = moteus.Controller(id=motor_id)
        self.running = True
    
    async def stop_motor(self):
        """Safely stop the motor"""
        await self.controller.set_stop()
        print("Motor stopped")
    
    async def position_control(self, position, velocity=0.2, accel=0.2):
        """
        Move to a target position
        
        Args:
            position: Target position in revolutions
            velocity: Maximum velocity in rev/s
            accel: Acceleration limit in rev/s^2
        """
        result = await self.controller.set_position(
            position=position,
            velocity=velocity,
            accel_limit=accel,
            query=True
        )
        return result
    
    async def velocity_control(self, velocity, accel=0.5):
        """
        Control motor at constant velocity
        
        Args:
            velocity: Target velocity in rev/s
            accel: Acceleration limit in rev/s^2
        """
        result = await self.controller.set_position(
            velocity=velocity,
            accel_limit=accel,
            query=True
        )
        return result
    
    async def torque_control(self, torque):
        """
        Apply constant torque
        
        Args:
            torque: Target torque in N⋅m
        """
        result = await self.controller.set_position(
            feedforward_torque=torque,
            query=True
        )
        return result
    
    async def monitor_status(self, duration=5.0):
        """Monitor motor status for a specified duration"""
        print(f"\nMonitoring motor for {duration} seconds...")
        print("Time(s) | Position(rev) | Velocity(rev/s) | Torque(Nm) | Temp(°C)")
        print("-" * 75)
        
        start_time = time.time()
        while time.time() - start_time < duration:
            result = await self.controller.query()
            elapsed = time.time() - start_time
            
            pos = result.values.get(moteus.Register.POSITION, 0)
            vel = result.values.get(moteus.Register.VELOCITY, 0)
            torque = result.values.get(moteus.Register.TORQUE, 0)
            temp = result.values.get(moteus.Register.TEMPERATURE, 0)
            
            print(f"{elapsed:6.2f}  | {pos:12.3f} | {vel:14.3f} | {torque:9.3f} | {temp:7.1f}")
            
            await asyncio.sleep(0.1)  # 10 Hz monitoring
    
    async def sinusoidal_motion(self, amplitude=0.5, frequency=0.2, duration=10.0):
        """
        Execute sinusoidal position trajectory
        
        Args:
            amplitude: Motion amplitude in revolutions
            frequency: Frequency in Hz
            duration: Total duration in seconds
        """
        print(f"\nExecuting sinusoidal motion: amplitude={amplitude} rev, freq={frequency} Hz")
        
        start_time = time.time()
        while time.time() - start_time < duration and self.running:
            t = time.time() - start_time
            target_pos = amplitude * math.sin(2 * math.pi * frequency * t)
            
            await self.controller.set_position(
                position=target_pos,
                velocity=1.0,
                accel_limit=2.0,
                query=False
            )
            
            await asyncio.sleep(0.01)  # 100 Hz control loop
        
        await self.stop_motor()
    
    async def step_response_test(self, step_size=0.5):
        """Test step response to measure system dynamics"""
        print(f"\nPerforming step response test with step size: {step_size} rev")
        
        # Move to zero position first
        await self.position_control(0.0)
        await asyncio.sleep(2)
        
        # Start monitoring and apply step
        monitor_task = asyncio.create_task(self.monitor_status(5.0))
        await asyncio.sleep(0.5)  # Small delay before step
        await self.position_control(step_size, velocity=1.0, accel=2.0)
        await monitor_task
    
    async def interactive_control(self):
        """Interactive control mode"""
        print("\n=== Interactive Motor Control ===")
        print("Commands:")
        print("  p <position>  - Move to position (revolutions)")
        print("  v <velocity>  - Run at velocity (rev/s)")
        print("  s             - Stop motor")
        print("  q             - Query status")
        print("  x             - Exit")
        print("=" * 40)
        
        # Note: This is a simplified version - in practice you'd want
        # to use proper async input handling or a separate thread
        await self.stop_motor()


async def demo_all_modes():
    """Demonstrate all control modes"""
    motor = MotorController(motor_id=1)
    
    try:
        print("=" * 60)
        print("MOTOR CONTROL DEMONSTRATION")
        print("=" * 60)
        
        # 1. Position Control Demo
        print("\n[1/4] Position Control Demo")
        positions = [0.0, 0.5, -0.5, 0.0]
        for pos in positions:
            print(f"Moving to position: {pos} rev")
            await motor.position_control(pos, velocity=0.3, accel=0.3)
            await asyncio.sleep(2)
        
        # 2. Monitor Status
        print("\n[2/4] Status Monitoring Demo")
        await motor.monitor_status(duration=3.0)
        
        # 3. Sinusoidal Motion
        print("\n[3/4] Sinusoidal Motion Demo")
        await motor.sinusoidal_motion(amplitude=0.3, frequency=0.5, duration=5.0)
        await asyncio.sleep(1)
        
        # 4. Step Response Test
        print("\n[4/4] Step Response Test")
        await motor.step_response_test(step_size=0.5)
        
        # Return to zero
        print("\nReturning to zero position...")
        await motor.position_control(0.0)
        await asyncio.sleep(2)
        
        await motor.stop_motor()
        print("\nDemo completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        await motor.stop_motor()
    except Exception as e:
        print(f"\nError: {e}")
        await motor.stop_motor()


async def simple_example():
    """Simple usage example for quick testing"""
    motor = MotorController(motor_id=1)
    
    try:
        # Move to a few positions
        await motor.position_control(0.5, velocity=0.2, accel=0.2)
        await asyncio.sleep(3)
        
        await motor.position_control(-0.2, velocity=0.2, accel=0.2)
        await asyncio.sleep(3)
        
        await motor.position_control(0.0, velocity=0.2, accel=0.2)
        await asyncio.sleep(2)
        
        await motor.stop_motor()
        
    except Exception as e:
        print(f"Error: {e}")
        await motor.stop_motor()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "simple":
        print("Running simple example...")
        asyncio.run(simple_example())
    else:
        print("Running full demonstration...")
        print("(Use 'python script.py simple' for quick test)")
        asyncio.run(demo_all_modes())
