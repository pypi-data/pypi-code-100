from atooms.system import System as _System


class System(_System):

    def compute_interaction(self, what='forces'):
        if not hasattr(self, 'interaction'):
            raise ValueError('system has no interaction')
        box = self.dump('cell.side', view=True)
        ids = self.dump('particle.species', view=True, dtype='int32')
        pos = self.dump('particle.position', order='F', view=True)
        self.interaction.compute(what, box, pos, ids)

    def _compute_neighbor_list(self):
        assert hasattr(self, 'neighbor_list'), 'system has no neighbor_list'
        box = self.dump('cell.side', view=True)
        ids = self.dump('particle.species', view=True, dtype='int32')
        pos = self.dump('particle.position', order='F', view=True)
        self.neighbor_list.compute(box, pos, ids)
        # Assign neighbors to particles
        nl = self.neighbor_list
        for i, p in enumerate(self.particle):
            p.neighbors = nl.neighbors[0: nl.number_neighbors[i], i]

