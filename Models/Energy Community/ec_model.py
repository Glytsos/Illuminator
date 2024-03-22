import mosaik_api

META = {
    'models': {
        'EnergyCommunity': {
            'public': True,
            'params': ['type', 'name', 'participants', 'energy_capacity', 'geographic_extent', 'hydrogen_storage_capacity', 'conversion_rate'],
            'attrs': ['size', 'energy_capacity', 'net_energy', 'energy_sold'],
        },
    },
}

class EnergyCommunitySimulator(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.data = {}
        self.energy_market_price = 0.1  # Fixed market price for simplicity
        # Predefined characteristics for small, medium, and large ECs
        self.ec_types = {
            'ECsmall': {'participants': 100, 'energy_capacity': 1, 'geographic_extent': 1, 'hydrogen_storage_capacity': 100, 'conversion_rate': 0.5},
            'ECmedium': {'participants': 1000, 'energy_capacity': 5, 'geographic_extent': 5, 'hydrogen_storage_capacity': 500, 'conversion_rate': 1},
            'EClarge': {'participants': 5000, 'energy_capacity': 20, 'geographic_extent': 20, 'hydrogen_storage_capacity': 1000, 'conversion_rate': 1.5},
        }

    def create(self, num, model, type, **kwargs):
        entities = []
        for i in range(num):
            eid = f'{type}_{i}'
            config = self.ec_types[type]
            config.update(kwargs)  # Allows for overriding default config
            self.data[eid] = EnergyCommunity(name=f'{type}_{i}', **config)
            entities.append({'eid': eid, 'type': model})
        return entities

    def step(self, time, inputs):
        current_hour = (time // 60) % 24
        for community in self.data.values():
            if 17 <= current_hour < 23:
                community.consume_hydrogen_sourced_electricity()
            community.sell_unused_capacity(self.energy_market_price)
        return time + 60

class EnergyCommunity:
    def __init__(self, name, participants, energy_capacity, geographic_extent, hydrogen_storage_capacity, conversion_rate):
        self.name = name
        self.participants = participants
        self.energy_capacity = energy_capacity
        self.geographic_extent = geographic_extent
        self.hydrogen_storage_capacity = hydrogen_storage_capacity
        self.conversion_rate = conversion_rate
        self.hydrogen_stored = hydrogen_storage_capacity
        self.energy_sold = 0
        self.net_energy = 0  # Initialize net energy

    def community_size(self):
        # Method to classify the community size (not used in this optimized version but useful for reporting)
        if self.participants <= 300:
            return 'Small'
        elif 300 < self.participants <= 3000:
            return 'Medium'
        else:
            return 'Large'

    def consume_hydrogen_sourced_electricity(self):
        if self.hydrogen_stored > 0:
            self.hydrogen_stored -= 1
            self.net_energy += self.conversion_rate

    def sell_unused_capacity(self, market_price):
        if self.net_energy > 0:
            self.energy_sold += self.net_energy * market_price
            self.net_energy = 0

if __name__ == '__main__':
    mosaik_api.start_simulation(EnergyCommunitySimulator())
