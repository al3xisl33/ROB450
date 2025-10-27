# Motor Control Scripts for Moteus Controller

These scripts provide programmatic control of your MAD-5005 motor using the moteus controller.

## Setup

Based on your documentation, you should already have the environment set up. If not:

```bash
# SSH into your Raspberry Pi
ssh -Y rob450@141.213.103.26
# Password: i<3robots!

# Navigate to your working directory
cd ./src/ROB450

# Activate the virtual environment
source moteus-venv/bin/activate

# Verify moteus is installed
python3 -c "import moteus; print('Moteus installed successfully')"
```

## Scripts Included

### 1. `motor_position_control.py` - Basic Position Control
Simple script demonstrating basic position control commands.

**Run it:**
```bash
python3 motor_position_control.py
```

**What it does:**
- Moves motor to position 0.5 revolutions
- Moves to position -0.2 revolutions
- Queries motor status
- Runs through a sequence of positions

### 2. `motor_control_advanced.py` - Advanced Control
Full-featured control with multiple modes and monitoring.

**Run it:**
```bash
# Full demonstration (all modes)
python3 motor_control_advanced.py

# Quick simple test
python3 motor_control_advanced.py simple
```

**Features:**
- Position control
- Velocity control
- Torque control
- Real-time status monitoring
- Sinusoidal trajectory generation
- Step response testing

## Key Control Commands

### Position Control
```python
await controller.set_position(
    position=0.5,      # Target position (revolutions)
    velocity=0.2,      # Max velocity (rev/s)
    accel_limit=0.2,   # Acceleration limit (rev/s²)
    query=True         # Request feedback
)
```

### Velocity Control
```python
await controller.set_position(
    velocity=0.5,      # Target velocity (rev/s)
    accel_limit=0.5,   # Acceleration limit
    query=True
)
```

### Torque Control
```python
await controller.set_position(
    feedforward_torque=0.1,  # Torque in N⋅m
    query=True
)
```

### Stop Motor
```python
await controller.set_stop()
```

### Query Status
```python
result = await controller.query()
position = result.values[moteus.Register.POSITION]
velocity = result.values[moteus.Register.VELOCITY]
torque = result.values[moteus.Register.TORQUE]
temperature = result.values[moteus.Register.TEMPERATURE]
```

## Customization Tips

### Change Motor ID
If your motor is not on ID 1, change it when creating the controller:
```python
controller = moteus.Controller(id=2)  # For motor ID 2
```

### Adjust Movement Parameters
- **velocity**: Max speed (typical: 0.1 to 2.0 rev/s)
- **accel_limit**: How quickly to accelerate (typical: 0.1 to 5.0 rev/s²)
- **position**: Target position in revolutions (can be negative)

### Safety Limits
Your documentation shows you set position limits to NAN in Tview. To add software limits:

```python
# Before moving
MIN_POSITION = -1.0  # revolutions
MAX_POSITION = 1.0   # revolutions

if position < MIN_POSITION or position > MAX_POSITION:
    print("Position out of bounds!")
    return
```

## Creating Your Own Script

Basic template:

```python
#!/usr/bin/env python3
import asyncio
import moteus

async def main():
    controller = moteus.Controller(id=1)
    
    try:
        # Your control logic here
        await controller.set_position(
            position=0.5,
            velocity=0.2,
            accel_limit=0.2
        )
        await asyncio.sleep(2)
        
        # Stop when done
        await controller.set_stop()
        
    except KeyboardInterrupt:
        await controller.set_stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## Troubleshooting

### Motor not moving
1. Check that motor is powered
2. Verify CAN bus connection
3. Ensure correct motor ID
4. Run `d stop` in Tview to clear any errors
5. Check for fault codes:
   ```python
   result = await controller.query()
   print(f"Fault: {result.values.get(moteus.Register.FAULT, 0)}")
   ```

### Permission errors
```bash
# May need to add user to dialout group
sudo usermod -a -G dialout $USER
# Then log out and back in
```

### Import errors
```bash
# Verify virtual environment is activated
source moteus-venv/bin/activate

# Reinstall if needed
pip install moteus --break-system-packages
```

## Motor Specifications (MAD-5005)

Based on your calibration output:
- **Poles:** 28
- **Resistance:** 0.164 ohms
- **Inductance:** 43.08 µH
- **Kv:** 269.5 rpm/V
- **Encoder:** Integrated

## Next Steps

1. Start with `motor_position_control.py` to verify basic functionality
2. Modify the position/velocity values to suit your application
3. Use `motor_control_advanced.py` as a reference for more complex control
4. Build your own custom control script based on your specific needs

## Safety Notes

⚠️ **Important Safety Reminders:**
- Ensure motor can spin freely before running scripts
- Start with slow velocities and accelerations
- Keep emergency stop accessible
- Monitor motor temperature during extended operation
- Test in a safe environment first

## Resources

- [Moteus Reference Manual](https://github.com/mjbots/moteus/blob/main/docs/reference.md)
- [Moteus Python Library Docs](https://github.com/mjbots/moteus/tree/main/lib/python)
- [Pi3Hat Documentation](https://github.com/mjbots/pi3hat)

## Your System Info

- **Pi IP:** 141.213.103.26
- **Username:** rob450
- **Motor ID:** 1 (assumed - verify in Tview)
- **Virtual Environment:** ~/moteus-venv
