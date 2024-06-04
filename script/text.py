def generate_signals_txt(data):
    signal_length = max(len(signal['name']) for signal in data['signals'])
    type_lengt = max(len(signal['type']) for signal in data['signals'])
    range_values_lenght = max(len(', '.join(data['defines'][signal['values']])) if 'values' in signal else len(str(signal['range'])) for signal in data['signals'])
    description_length = max(len(signal['comment']) for signal in data['signals'])

    with open('../lib/signals/signals.txt', 'w') as file:
        file.write(f"{'Signal':<{signal_length}} | {'Type':<{type_lengt}} | {'Range/Values':<{range_values_lenght}} | {'Description':<{description_length}}\n")
        file.write('-' * (signal_length + type_lengt + range_values_lenght + description_length + 9) + '\n')
        
        for signal in data['signals']:
            name = signal['name']
            type_ = signal['type']
            range_values = ', '.join(data['defines'][signal['values']]) if 'values' in signal else str(signal['range'])
            description = signal['comment']
            file.write(f"{name:<{signal_length}} | {type_:<{type_lengt}} | {range_values:<{range_values_lenght}} | {description:<{description_length}}\n")

