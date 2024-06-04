def generate_test_cases(data):
    with open('../test/test.cpp', 'w') as f:
        f.write('#include "signals.h" \n')
        f.write('#include <gtest/gtest.h> \n\n')

        for signal in data['signals']:
            f.write(f"TEST(test_signal, test_{signal['name']})\n{{\n")
            f.write(f"\t{signal['type']} value;\n")
            if 'range' in signal:
                f.write(f"\tvalue = {signal['range'][0]};\n")
            else:
                f.write(f"\tvalue = {data['defines'][signal['values']][0]};\n")
            f.write(f"\tEXPECT_TRUE(signals_set_{signal['name']}(value));\n")
            if signal['type'] in ['float', 'double']:
                f.write(f"\tEXPECT_NEAR(value, signals_get_{signal['name']}(), PRECISION);\n\n")
            else:
                f.write(f"\tEXPECT_EQ(value, signals_get_{signal['name']}());\n\n")

            if 'range' in signal:
                f.write(f"\tvalue = {signal['range'][-1]};\n")
            else:
                f.write(f"\tvalue = {data['defines'][signal['values']][-1]};\n")
            f.write(f"\tEXPECT_TRUE(signals_set_{signal['name']}(value));\n")

            if signal['type'] in ['float', 'double']:
                f.write(f"\tEXPECT_NEAR(value, signals_get_{signal['name']}(), PRECISION);\n\n")
            else:
                f.write(f"\tEXPECT_EQ(value, signals_get_{signal['name']}());\n\n")

            if 'range' in signal:
                f.write(f"\tvalue = {signal['range'][-1]} + 1;\n")
            else:
                f.write(f"\tvalue = {data['defines'][signal['values']][-1]} + 1;\n")
            f.write(f"\tEXPECT_FALSE(signals_set_{signal['name']}(value));\n")

            if 'range' in signal and signal['range'][0] > 0 or signal['type'] in ['float', 'double', 'int', 'int8_t', 'int16_t', 'int32_t', 'int64_t']:
                f.write(f"\n\tvalue = {signal['range'][0]} - 1;\n")
                f.write(f"\tEXPECT_FALSE(signals_set_{signal['name']}(value));\n")
            
            f.write(f'}}\n\n')