# ARP_MitM_ATTACK
Herramienta desarrollada en Python y Scapy para ejecutar ataques Man-in-the-Middle (MITM) mediante envenenamiento de tablas ARP (ARP Spoofing) en redes LAN.

# 💎 Herramienta de Intercepción: ARP Spoofing 
**Desarrollado por:** Abi.R (Matrícula 2024-1179)
**Asignatura:** Seguridad Informática

## 🧐 El Protocolo ARP
**ARP (Address Resolution Protocol)** es el protocolo encargado de traducir direcciones IP (Lógicas) a direcciones MAC (Físicas).

En una red local, cuando un equipo quiere enviar datos a una IP (ej. `20.24.11.1`), primero necesita saber qué tarjeta de red física (MAC Address) tiene esa IP. ARP hace la pregunta a la red: *"¿Quién tiene la IP X?"* y el dueño responde.

### La Vulnerabilidad
El problema de diseño es que **ARP no tiene validación**. Es un protocolo "confiado":
1.  Cualquier dispositivo puede responder a una pregunta ARP, incluso si no es el dueño real de la IP.
2.  Un dispositivo aceptará una actualización de información ("Gratuitous ARP") incluso si nunca hizo una pregunta.
3.  La última respuesta recibida siempre sobrescribe a la anterior.

### Funcionamiento de la Herramienta
El script explota esta debilidad enviando respuestas falsificadas constantemente:
1.  Le dice a la **Víctima** que la MAC del Router es la del Atacante.
2.  Le dice al **Router** que la MAC de la Víctima es la del Atacante.
3.  Al situarse en el medio, el atacante puede leer, modificar o bloquear el tráfico (Man-in-the-Middle).

---

## ⚙️ Configuración del Entorno (Topología)

La infraestructura simula una red corporativa funcional con salida a Internet real.

### 1. Router R1 (Gateway)
* **Interfaz:** `Ethernet0/0` (LAN)
* **Dirección IP:** `20.24.11.1`
* **Función:** Gateway para salida a Internet (NAT) y Servidor DHCP.

### 2. PC1 (Víctima)
* **Interfaz:** `eth0`
* **Dirección IP:** *Dinámica (DHCP)*
* **Rango:** `20.24.11.x`
* **Gateway:** `20.24.11.1`
* **Descripción:** Simula un usuario legítimo navegando en Internet.

### 3. Kali Linux (Atacante)
* **Interfaz:** `eth0`
* **Dirección IP:** `20.24.11.20` (Estática)
* **Requisito Crítico:** Debe tener habilitado el reenvío de paquetes (IP Forwarding) para no cortar la conexión de la víctima.

---

## 🛠️ Desarrollo e Implementación Técnica
Esta herramienta fue desarrollada en **Python 3** utilizando la librería **Scapy**.

Se utilizan **Paquetes Crudos (Raw Packets)** para construir manualmente las tramas ARP. Esto permite falsificar el campo "Sender MAC Address" dentro del paquete, algo que el sistema operativo bloquearía en una conexión normal. El script envía estos paquetes en un bucle infinito para luchar contra el mecanismo de "auto-corrección" de la red.

---

## 🚀 Guía de Uso Paso a Paso

### Paso 1: Habilitar IP Forwarding (Importante) 
Antes de atacar, debemos configurar nuestro Kali Linux para que actúe como un router y deje pasar el tráfico de la víctima hacia Internet. Si omitimos este paso, le cortaremos el Internet a la víctima (DoS) en lugar de espiarla.

```bash echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward ```

### Paso 2: Verificar Estado Inicial (En la Víctima) En la PC víctima, verificamos la tabla ARP para ver la dirección MAC legítima del Router antes del ataque. 

```bash PC1> show arp ```

### Paso 3: Ejecución del Ataque Ejecutamos el script con permisos de administrador. 
```bash sudo python3 atack_arp_abi.py ```

### Paso 4: Verificación del Envenenamiento
```bash sudo python3 atack_arp_abi.py ```

### 🛡️ Medidas de Mitigación

Para prevenir la suplantación ARP en redes empresariales, se recomienda implementar Dynamic ARP Inspection (DAI) en los switches.

Esta función de seguridad utiliza la base de datos del DHCP Snooping para validar que cada respuesta ARP provenga realmente del dispositivo autorizado, descartando automáticamente las respuestas falsificadas por atacantes.

### Comandos:
Switch(config)# ip dhcp snooping
Switch(config)# ip dhcp snooping vlan 1
Switch(config)# ip arp inspection vlan 1


