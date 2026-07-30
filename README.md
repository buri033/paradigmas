# 🦆 DuckBank - Banca en Línea

¡Bienvenido a la documentación inicial de **DuckBank**!

El proyecto fue creado utilizando HTML, CSS y JavaScript para el desarrollo del MVP de la aplicación bancaria DuckBank.

---

## 📁 Estructura del Proyecto

La arquitectura del proyecto está organizada por carpetas, manteniendo un archivo HTML independiente por pantalla en la raíz y separando los estilos e interacciones en las carpetas `/css` y `/js`:

```text
paradigmas/
├── index.html              # Dashboard Principal
├── login.html              # Inicio de Sesión
├── register.html           # Registro de Usuario
├── forgot-password.html    # Recuperación de Contraseña
├── transfers.html          # Transferencias Monetarias
├── savings.html            # Cuenta de Ahorros y Metas
├── cards.html              # Tarjetas de Crédito (Diseño Plano)
├── loans.html              # Gestión de Créditos Activos
├── simulator.html          # Simulador de Préstamos
├── investments.html        # Portafolio de Inversiones
├── applications.html       # Solicitud de Productos
├── admin.html              # Panel Administrativo
├── README.md               # Documentación del Proyecto
├── css/
│   ├── variables.css       # Variables de color y diseño
│   ├── common.css          # Layout, Sidebar, Header, Botones, Tablas y Toast
│   ├── auth.css            # Estilos de autenticación
│   ├── dashboard.css       # Estilos de balance, gráficos y accesos rápidos
│   ├── transfers.css       # Estilos de transferencias y agenda de contactos
│   ├── savings.css         # Estilos de metas de ahorro
│   ├── cards.css           # Estilos de tarjetas planas
│   ├── loans.css           # Estilos de barra de progreso de créditos
│   ├── simulator.css       # Estilos de sliders del simulador
│   ├── investments.css     # Estilos de fondos de inversión
│   ├── applications.css    # Estilos del catálogo de productos
│   └── admin.css           # Estilos de métricas y gestión administrativa
└── js/
    ├── common.js           # Menú activo, Notificaciones Toast, Formateador CLP
    ├── auth.js             # Validaciones de login/registro
    ├── dashboard.js        # Animaciones de saldo
    ├── transfers.js        # Lógica de transferencia y modal comprobante
    ├── savings.js          # Creador de metas de ahorro
    ├── cards.js            # Visibilidad CVV, bloqueo y pago de tarjeta
    ├── loans.js            # Pago de cuota de crédito
    ├── simulator.js        # Cálculo en tiempo real de cuota mensual y costo total
    ├── investments.js      # Selección e inversión en fondos mutuos
    ├── applications.js     # Asistente por pasos de solicitud digital
    └── admin.js            # Aprobación y rechazo en tiempo real de solicitudes
```

---

## 🛠️ Módulos y Funcionalidades Incluidas

1. **Dashboard Principal (`index.html`)**: Saldo total, accesos rápidos, gráfico semanal de ingresos vs gastos y transacciones recientes.
2. **Autenticación (`login.html`, `register.html`, `forgot-password.html`)**: Formularios de inicio de sesión, registro y recuperación de clave.
3. **Transferencias (`transfers.html`)**: Contactos frecuentes, autocompletado y comprobante de transacción.
4. **Cuenta de Ahorros (`savings.html`)**: Registro de intereses y metas de ahorro con barra de progreso.
5. **Tarjetas de Crédito (`cards.html`)**: Tarjetas digitales en diseño plano, visualización de CVV, bloqueo temporal y pago de cupo.
6. **Créditos (`loans.html`)**: Estado de préstamos activos, progreso de cuotas y tabla de vencimientos.
7. **Simulador de Préstamos (`simulator.html`)**: Sliders de monto y plazo con cálculo de cuota mensual y costo total.
8. **Inversiones (`investments.html`)**: Catálogo de Fondos Mutuos e historial de aportes.
9. **Solicitud de Productos (`applications.html`)**: Selección de productos financieros y formulario de evaluación.
10. **Panel de Admin (`admin.html`)**: Métricas operacionales y tabla para aprobar o rechazar solicitudes.

---

## 🚀 Cómo Ejecutar el Proyecto Localmente

1. Clona o descarga este repositorio.
2. Abre cualquier archivo `.html` (como `index.html` o `login.html`) directamente en tu navegador web.
