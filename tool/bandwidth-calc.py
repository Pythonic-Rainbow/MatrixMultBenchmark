choice = int(input(
    '1. PCIe\n'
    '2. VRAM\n'
))

if choice == 1:
    link_speed = float(input('Enter link speed in GHz: '))
    lane_count = int(input('Enter number of lanes: '))
    print(link_speed * 128/130 * lane_count)  # 128/130 is the encoding scheme of PCIe Gen3+
elif choice == 2:
    clock_speed = float(input('Enter clock speed in GHz: '))
    bus_width = int(input('Enter bus width in bits: '))
    pump_rate = int(input('Enter pump rate: '))
    print(clock_speed * bus_width * pump_rate)