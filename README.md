# Proyecto SO_P1_2025 — Simulación de Planificador Multinivel (MLQ)

**Autor:** Deysi Yuliana Rivas Varela
**Universidad del Valle**  
**Curso:** Sistemas Operativos  
**Periodo:** 2025-2  

## Descripción
Simulación de un planificador de CPU con **colas multinivel (MLQ)** con tres políticas:
- Cola 1 → Round Robin (quantum = 1)
- Cola 2 → Round Robin (quantum = 3)
- Cola 3 → Shortest Job First (SJF)

El programa lee archivos de entrada con el formato:
# Archivo: mlq001.txt
# etiqueta; burst time (BT); arrival time (AT); Queue (Q); Priority (5 > 1)
A; 6; 0; 1; 5
B; 9; 0; 1; 4
C; 10; 0; 2; 3
D; 15; 0; 2; 3
E; 8; 0; 3; 2

# genera una tabla con métricas: WT, CT, RT, TAT, junto con los promedios.
Etiqueta;BT;AT;Q;Pr;WT;CT;RT;TAT
A;6;0;1;5;5;11;0;11
B;9;0;1;4;6;15;1;15
C;10;0;2;3;24;34;15;34
D;15;0;2;3;25;40;18;40
E;8;0;3;2;40;48;40;48

Promedios: WT=20.00; CT=29.60; RT=14.80; TAT=29.60