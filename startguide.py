from deltakit import Client

from deltakit_circuit import Coord2D
from deltakit_explorer.codes import css_code_memory_circuit, RepetitionCode, RotatedPlanarCode
from deltakit_circuit.gates import PauliBasis
Client.set_token("GGuRx95pgWcws5ILnhwC_5nt2K5F9S6U")

cloud = Client.get_instance()

#two basic errors are:

# Bit flip (X): 0↔1, the arrow flipped top to bottom
# Phase flip (Z): a flip that only exists in quantum, where the arrow spins around the equator


# distance parameter is for how many qubits you store one logicla bit?
#bigger repition codes give lower logical error rates

#distance 3 means 0-> 000
rep_code = RepetitionCode(distance=3, stabiliser_type=PauliBasis.Z)

circuit = css_code_memory_circuit(
    css_code=rep_code,
    num_rounds=3,
    logical_basis=PauliBasis.Z,  # Z-basis stabilisers protect from bit flips
)

#  stabiliser means helpers ask z type parity
#  compairng 1->2 2->3 adds 1 each 
#  so 5 total?

print(len(circuit.qubits))  # gives 5 so yes




stim_circuit = circuit.as_stim_circuit()

#readable text version
text_stim_circuit = str(stim_circuit)
print(text_stim_circuit)
text_qasm_circuit = stim_circuit.to_qasm(open_qasm_version=3, skip_dets_and_obs=True)

stim_circuit.diagram("timeline-svg-html")

from deltakit_circuit import gates
from deltakit_decode.noise_sources import StimNoise
from deltakit_explorer.qpu import QPU, NativeGateSetAndTimes, ToyNoise, NoiseParameters


qpu_instance = QPU(
    qubits=circuit.qubits,  # only qubits we need are defined
    native_gates_and_times=NativeGateSetAndTimes(
        # times are given approximately for a superconducting device
        one_qubit_gates={gates.H: 20e-9, gates.SQRT_X: 20e-09},
        two_qubit_gates={gates.CZ: 30e-9},
        reset_gates={gates.RZ: 160e-9},
        measurement_gates={gates.MZ: 500e-9, gates.MRZ: 500e-9},
    ),
    # let's keep it noiseless for now, you may omit this line
    noise_model=NoiseParameters(),
)

deltakit_compiled_circuit = qpu_instance.compile_circuit(circuit)