"""
Proyecto finsl: Fibrosis pulmonar

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
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0, t0, tend, dt, w, h = 0, 0, 30, 1E-3, 6, 3
N = round((tend - t0) / dt) + 1
t = np.linspace(t0, tend, N)

# Señales de entrada para paciente sano y enfermo
u1 = 1 * np.sin(2 * m.pi * t)  # Paciente sano (amplitud 1 y frecuencia 2*pi)
u2 = 0.4 * np.sin(2 * m.pi * t)  # Paciente enfermo (amplitud 0.4 y frecuencia 2*pi)

# Función de transferencia basada en el modelo del lazo abierto proporcionado
def sys_model(L, R1, R2, R3, C):
    a0 = R1 + R3
    a1 = L + C*(R1*R2 + R1*R3 + R2*R3)
    a2 = L*C*(R2+R3)
    return ctrl.tf([R3], [a2, a1, a0])

# Parámetros del sistema para paciente sano y enfermo
L = 10e-3
R1_sano, R2_sano, R3_sano, C_sano = 30, 60, 60, 100e-6
sysS = sys_model(L, R1_sano, R2_sano, R3_sano, C_sano)
print('Individuo sano [control]:')
print(sysS)

R1_enf, R2_enf, R3_enf, C_enf = 120, 10, 60, 10e-6
sysE = sys_model(L, R1_enf, R2_enf, R3_enf, C_enf)
print('Individuo enfermo [caso]:')
print(sysE)

def plot_combined_signals(t, sysS, u1, sysE, u2, sysPID, u_treatment):
    fig = plt.figure()
    # Respuesta paciente sano
    ts, Vs = ctrl.forced_response(sysS, t, u1, x0)
    plt.plot(t, Vs, '-', color=[0.1, .5, .7], label='$V_s(t): Control$')
    # Respuesta paciente enfermo
    ts, Ve = ctrl.forced_response(sysE, t, u2, x0)
    plt.plot(t, Ve, '-', color=[1, 0, 0], label='$V_s(t): Caso$')
    # Respuesta tratamiento en lazo cerrado con entrada u_treatment (escalada para igualar amplitud)
    ts, pid = ctrl.forced_response(sysPID, t, u_treatment, x0)
    plt.plot(t, pid, ':', linewidth=3, color=[0.6, .2, .5], 
             label='$V_s(t): Tratamiento$') 
    plt.grid(False)
    plt.xlim(0, 30)
    plt.ylim(-1, 1)
    plt.xticks(np.arange(0, 31, 2))
    plt.yticks(np.arange(-1, 1.1, 0.5))
    plt.xlabel('$t$ [s]')
    plt.ylabel('$V_s(t)$')
    plt.legend(bbox_to_anchor=(0.5, -0.3), loc='center', ncol=3,
               fontsize=8, frameon=False)
    fig.set_size_inches(w, h)
    fig.tight_layout()
    plt.show()
    namepng = 'python_combined.png'
    namepdf = 'python_combined.pdf'
    fig.savefig(namepng, dpi=600, bbox_inches='tight')
    fig.savefig(namepdf, bbox_inches='tight')

# Controlador Integral puro con ganancia I = 1929.48273797327
def controlador_integral(Ki):
    # Transferencia de un integrador multiplicado por Ki: Ki/s
    return ctrl.tf([Ki], [1, 0])

# Crear sistema controlado en lazo cerrado con controlador integral
Ki = 1929.48273797327
C = controlador_integral(Ki)

# Formar sistema en serie controlador × sistema enfermo
sistema_abierto = ctrl.series(C, sysE)
# Realizar retroalimentación unitaria negativa para lazo cerrado
sysPID = ctrl.feedback(sistema_abierto, 1, sign=-1)

# Obtener la respuesta del paciente sano para medir amplitud máxima
_, Vs = ctrl.forced_response(sysS, t, u1, x0)
V1_max = np.max(np.abs(Vs))

# Obtener la respuesta del tratamiento con la entrada original para medir amplitud máxima
_, pid_sin_escala = ctrl.forced_response(sysPID, t, u1, x0)
pid_max = np.max(np.abs(pid_sin_escala))

# Calcular factor de escala para entrada al tratamiento para igualar amplitud
factor_escala = V1_max / pid_max if pid_max != 0 else 1

# Escalar la señal de entrada para el sistema en lazo cerrado
u_treatment = factor_escala * u1

print(f"Amplitud paciente sano: {V1_max:.4f}")
print(f"Amplitud tratamiento sin escalar: {pid_max:.4f}")
print(f"Factor de escala aplicado a la entrada del tratamiento: {factor_escala:.4f}")

# Graficar señales combinadas en mismo gráfico, la entrada del tratamiento es la señal escalada para igualar la amplitud
plot_combined_signals(t, sysS, u1, sysE, u2, sysPID, u_treatment)