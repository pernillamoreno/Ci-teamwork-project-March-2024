def generate_signal_func(data):
    import math
    bit_len = sum([signal['length'] for signal in data['signals']])
    byte_len = math.ceil(bit_len / 8)
    with open('../lib/signals/signals.cpp', 'w') as f:
        f.write('#include "signals.h"\n#include "buffer.h"\n#include <type_traits>\n\n')
        f.write(f"static uint8_t buffer[{byte_len}]{{0}};\n\n")

        for signal in data['signals']:
            # set signal
            f.write(f"bool signals_set_{signal['name']}({signal['type']} value)\n{{\n")
            f.write(f"\tbool status{{false}};\n")
            if 'range' in signal:
                if signal['range'][0] == 0 and signal['type'] not in ['float', 'double']:
                    f.write(f"\tif(value <= {signal['range'][-1]}){{\n")
                else:
                    f.write(f"\tif(value >= {signal['range'][0]} && value <= {signal['range'][-1]}){{\n")
            else:
                f.write(f"\tif(value <= {data['defines'][signal['values']][-1]}){{\n")
            
            f.write(f"\t\tstatus = true;\n")
            if signal['type'] in ['float', 'double']:
                f.write(f"\t\tbuffer_insert(buffer, {signal['start']}, {signal['length']}, value / PRECISION);\n\t}}\n")
            else:
                f.write(f"\t\tbuffer_insert(buffer, {signal['start']}, {signal['length']}, value);\n\t}}\n")
            f.write(f"\treturn status;\n}}\n\n")

            # get signal
            f.write(f"{signal['type']} signals_get_{signal['name']}(void)\n{{\n")        
            if signal['type'] not in ['uint8_t', 'uint16_t', 'uint32_t', 'uint64_t']:
                f.write(f"\tuint32_t value{{buffer_extract(buffer, {signal['start']}, {signal['length']})}};\n")
                f.write(f"\tif(value & (1u << {signal['length'] - 1})){{\n")
                f.write(f"\t\tvalue |= (~0u) << {signal['length']};\n\t}}\n")
                if signal['type']in ['float', 'double']:
                    f.write(f"\treturn (static_cast<{signal['type']}>(static_cast<int32_t>(value)) * PRECISION);\n}}\n\n")
                else:
                    f.write(f"\treturn static_cast<{signal['type']}>(value);\n}}\n\n")
            else:
                f.write(f"\treturn static_cast<{signal['type']}>(buffer_extract(buffer, {signal['start']}, {signal['length']}));\n}}\n\n")
