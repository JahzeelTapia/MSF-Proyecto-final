"""
Proyecto final: Fibrosis pulmonar

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Jahzeel Abisai Tapia Gracia
Número de control: 22210798
Correo institucional: l22210798@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
t0, tF, dt = 0, 30, 1e-3
t = np.arange(t0, tF+dt, dt)
f = 0.5  # Hz
u = np.sin(2 * math.pi * f * t)

# Modelo de transferencia
def sys_model(L, R1, R2, R3, C):
    a0 = R1 + R3
    a1 = L + C*(R1*R2 + R1*R3 + R2*R3)
    a2 = L*C*(R2+R3)
    return ctrl.tf([R3], [a2, a1, a0])

# Parámetros
L = 10e-3
# Paciente sano
R1_sano, R2_sano, R3_sano, C_sano = 30, 60, 60, 100e-6
sys_sano = sys_model(L, R1_sano, R2_sano, R3_sano, C_sano)
# Paciente enfermo
R1_enf, R2_enf, R3_enf, C_enf = 120, 10, 60, 10e-6
sys_enf  = sys_model(L, R1_enf,  R2_enf,  R3_enf,  C_enf)

t1, y1 = ctrl.forced_response(sys_sano, T=t, U=u)
t2, y2 = ctrl.forced_response(sys_enf,  T=t, U=u)

plt.figure(figsize=(8,4))

plt.plot(t1, y1, color='tab:red', linestyle='-', linewidth=2, label='Paciente sano')
plt.plot(t2, y2, color='tab:blue', linestyle='--', linewidth=2,label='Paciente enfermo')

plt.xlabel('Tiempo [s]')
plt.ylabel('$V_s(t)$')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
