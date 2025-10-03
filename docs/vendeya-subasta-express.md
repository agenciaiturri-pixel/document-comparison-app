# VendeYa – Subasta Express

## 1. Resumen Ejecutivo
VendeYa es una aplicación móvil tipo marketplace enfocada en subastas exprés de productos usados. Cada subasta dura un máximo de 24 horas para generar urgencia, rotación de inventario y participación diaria de la comunidad. La plataforma monetiza desde el lanzamiento mediante comisiones por venta y un modelo freemium con servicios destacados. La propuesta combina experiencia de subastas ultrarrápidas, pagos seguros y geolocalización inteligente para posicionarse como la opción preferida de reventa ágil en Latinoamérica.

### 1.1 Contexto y Oportunidad
- Crecimiento sostenido de la economía circular y del mercado de segunda mano en la región.
- Usuarios jóvenes demandan experiencias móviles inmediatas, seguras y entretenidas.
- Falta de alternativas de subastas con liquidez alta y tiempos acotados que otorguen certidumbre al vendedor.

### 1.2 Diferenciadores Clave
- Única duración de subasta (24h) que simplifica decisiones y acelera rotación.
- Protección transaccional end-to-end sin abandonar la app.
- Gamificación y recompensas que fomentan la recurrencia diaria.

## 2. Objetivos del Negocio
- Permitir que cualquier persona venda un producto usado en menos de 24 horas.
- Cobrar una comisión por cada transacción completada (5%–10%).
- Construir una comunidad activa con uso recurrente diario.
- Generar ingresos inmediatos con planes freemium, comisiones y productos destacados.
- Alcanzar el punto de equilibrio en 12 meses con 30 mil usuarios activos mensuales y ticket promedio de S/120.
- Lograr NPS ≥ 55 y tasa de resolución de disputas > 90% en menos de 72 horas.

## 3. Propuesta de Valor
- Subastas rápidas y sencillas con publicación en menos de un minuto.
- Sistema de pujas en tiempo real con extensión anti-sniping en los últimos minutos.
- Pagos seguros con retención de fondos hasta la confirmación de entrega.
- Geolocalización para encontrar productos cercanos y facilitar entregas personales.

## 4. Audiencia Objetivo
- Personas que desean vender productos usados rápidamente.
- Compradores que buscan ofertas dinámicas y subastas cortas.
- Emprendedores y pequeños negocios con stock limitado o remanente.

### 4.1 Personas Principales
1. **Laura, la cazadora de ofertas (28 años)**
   - Vive en zonas urbanas, compra moda y accesorios semanalmente.
   - Necesita alertas instantáneas y chat rápido para coordinar entregas cerca.
2. **Carlos, el revendedor tecnológico (33 años)**
   - Renueva gadgets con frecuencia, publica 3–5 artículos por semana.
   - Requiere flujo de publicación express, métricas de desempeño y reputación sólida.
3. **María, emprendedora de stock remanente (41 años)**
   - Negocio pequeño con inventario estacionario; busca liquidez inmediata.
   - Valora campañas destacadas, herramientas de promoción y conciliación de pagos clara.

## 5. Experiencia de Usuario
- Interfaz moderna, ágil y accesible con modo claro/oscuro.
- Registro simplificado mediante correo, Google o Facebook.
- Botones prominentes, iconografía clara y navegación intuitiva.
- Enfoque en tiempos de carga reducidos para listados y subastas.
- Microcopys claros que refuercen urgencia ("Quedan 2h 15m").
- Accesibilidad AA: contraste adecuado, soporte para lectores de pantalla, tamaños de toque ≥ 44px.

## 6. Flujo Principal del Vendedor
1. Registro e inicio de sesión con verificación básica.
2. Publicación rápida del producto:
   - Carga de 1 a 5 fotos (con recorte automático y compresión).
   - Título, descripción breve y categoría.
   - Precio inicial sugerido y precio mínimo opcional (alerta si es menor al 50% del precio promedio).
   - Ubicación automática (GPS) o manual con autocompletado.
   - Selección de servicios adicionales (destacado, difusión en redes).
   - Confirmación con el botón “Subastar por 24h”.
3. Monitoreo de pujas en tiempo real y chat con postores.
4. Recepción de notificaciones de pago asegurado y confirmación de entrega.
5. Evaluación mutua entre comprador y vendedor para fortalecer reputación.

## 7. Flujo Principal del Comprador
1. Registro e inicio de sesión (opción de invitado para explorar, sin pujar).
2. Exploración de subastas mediante home personalizada, búsqueda y filtros por categoría, ubicación, precio, tiempo restante y estado del producto.
3. Acceso a detalle de producto con fotos, descripción, reputación del vendedor, contador regresivo e historial de pujas.
4. Realización de puja con incrementos mínimos predefinidos (S/1.00 o $1.00) y confirmación biométrica cuando el dispositivo lo permita.
5. Chat con el vendedor una vez se haya realizado una puja, con mensajes predeterminados para agilizar consultas frecuentes.
6. Pago in-app al ganar la subasta y coordinación de entrega con selección de método.
7. Calificación del vendedor tras recibir el producto, con opción de abrir disputa.

## 8. Funcionalidades Clave
### 8.1 Publicación Rápida
- Validación de campos mínimos y soporte de múltiples categorías (electrónica, moda, hogar, libros, fitness, vehículos - solo partes -, otros).
- Límite de subasta a 24 horas.
- Previsualización inmediata del anuncio antes de publicar.
- Auto-sugerencias de título y precio con IA ligera basada en historial.

### 8.2 Subastas en Tiempo Real
- Contador regresivo visible con actualización en tiempo real.
- Incrementos mínimos automáticos por moneda y rango de precio.
- Extensión de 1 minuto si hay pujas en los últimos 3 minutos.
- Notificaciones inmediatas al ser superado o ganar.
- Historial de pujas transparente con alias y timestamp.

### 8.3 Pagos Seguros y Custodia
- Métodos soportados: tarjeta, billeteras digitales, otros medios locales.
- Retención de fondos hasta confirmación del vendedor.
- Liberación al vendedor tras confirmación del comprador o tras 3 días sin reclamo.
- Motor antifraude con validaciones de identidad y monitoreo de patrones de pago.

### 8.4 Geolocalización
- Ubicación automática mediante GPS.
- Filtros de distancia (1 km, 5 km, 10 km, país).
- Priorización de listados cercanos.
- Mapa interactivo para visualizar subastas próximas.

### 8.5 Chat Interno
- Disponible solo para usuarios que hayan realizado una oferta.
- Mensajería en tiempo real con notificaciones push.
- Historial asociado a la subasta específica.
- Filtros automáticos de spam y detección de contenido sensible.

### 8.6 Perfil de Usuario
- Foto o avatar, reseñas, historial de ventas/compras.
- Sistema de reputación con estrellas y comentarios.
- Validación opcional con DNI o número de celular.
- Badges por logros (vendedor confiable, respuesta rápida, entregas puntuales).

### 8.7 Notificaciones Push
- Pujas recibidas y superadas.
- Inicio y cierre de subasta.
- Nuevos productos en categorías favoritas.
- Promociones, logros de gamificación y actualizaciones.
- Recordatorios para completar pago, entrega y calificación.

### 8.8 Seguridad y Moderación
- Reporte de usuarios y publicaciones sospechosas.
- Moderación apoyada por IA o revisión manual.
- Bloqueo de categorías prohibidas (armas, medicamentos, productos ilegales/peligrosos).
- Auditoría interna para trazabilidad de cambios críticos.

### 8.9 Accesibilidad y Localización
- Traducciones iniciales: español neutro y portugués brasileño.
- Compatibilidad con lectores de pantalla iOS/Android.
- Soporte para formatos de moneda locales y múltiples impuestos.

## 9. Monetización
- Comisión por venta exitosa: 5%–10%.
- Productos destacados (S/2.00) para prioridad en listados.
- Publicación automática en redes sociales (S/1.50 opcional).
- Suscripción premium con comisión reducida, subidas ilimitadas, mayor visibilidad y chat sin pujar.
- Bonos por invitación y gamificación (rachas, rankings, estrellas semanales).
- Marketplace de servicios de logística asociados (comisión por lead derivado).
- Publicidad nativa controlada para marcas alineadas.

### 9.1 Proyecciones Financieras Iniciales (12 meses)
- Usuarios registrados: 120k.
- Usuarios activos mensuales: 30k.
- Ratio conversión visita → puja: 12%.
- Ticket promedio: S/120.
- Ingreso bruto estimado: S/2.16M.
- Ingreso neto por comisiones (7% promedio): S/151k.
- Ingreso complementario (premium + destacados): S/96k.

## 10. Logística y Entrega
- Entrega personal coordinada vía chat.
- Integración opcional con operadores logísticos locales (courier) con cálculo de envío por distancia.
- Cobro del costo de envío incluido en el flujo de pago.
- Seguimiento de envío con estados: pendiente, en tránsito, entregado.
- Seguros opcionales para envíos de alto valor.

## 11. Estadísticas para Usuarios
- Vendedores: visitas por producto, número de pujas, subastas ganadas.
- Compradores: historial de compras, ranking de pujas perdidas.
- Panel de desempeño con conversiones de destacados y ROI estimado.
- Insights automáticos (mejor hora para publicar, categorías con mayor demanda).

## 12. Panel de Administración Interno
- Visualización de subastas activas y finalizadas.
- Moderación de contenido ofensivo o reportado.
- Gestión de usuarios y sanciones.
- Configuración de comisiones, tiempos, promociones y destacados.
- Herramientas de soporte para intervenir en disputas y liberar pagos manualmente.
- Reportes descargables (CSV/BI) para equipo financiero y marketing.

## 13. Soporte y Mediación
- Centro de ayuda con preguntas frecuentes.
- Chatbot con IA 24/7.
- Soporte por correo para disputas con sistema de mediación.
- Protocolos claros de respuesta en < 4h para incidentes críticos.
- Base de conocimiento auto-gestionable para el equipo de soporte.

## 14. Lanzamiento por Fases
1. **Fase 1:** Beta en una sola ciudad (Trujillo o Lima).
   - Objetivo: 5k usuarios registrados, 1k productos subastados, feedback cualitativo.
   - Acciones: campañas con influencers locales, alianzas con comunidades universitarias.
2. **Fase 2:** Escalado a más ciudades con envíos nacionales.
   - Objetivo: 40k usuarios, logística integrada y suscripciones premium.
   - Acciones: partnerships con couriers, campañas pagadas en redes, referidos.
3. **Fase 3:** Incorporación de tiendas locales con stock remanente.
   - Objetivo: monetización B2B, programas de fidelización y catálogo ampliado.
   - Acciones: fuerza comercial, API para subir inventarios masivos, eventos de subastas en vivo.

## 15. Identidad de Marca
- Nombre: **VendeYa**.
- Slogan: “Lo tuyo, vendido en 24 horas”.
- Paleta: naranja, negro, blanco.
- Estilo: urbano, moderno, mercado digital ágil.
- Logo sugerido: carrito de compra con reloj integrado.
- Voz de marca cercana, energética, confiable.
- Sistema de diseño modular para escalabilidad (componentes: cards, badges, timers, chips de filtro).

## 16. Roadmap Futuro
- Subastas en vivo estilo TikTok Live.
- Tiendas verificadas con sello dorado.
- Moneda interna “VendeYa Coins”.
- Programas de protección al comprador tipo seguro.
- Inteligencia de precios dinámica según demanda.
- Integración con marketplaces aliados y canales sociales.

## 17. Estrategia de Producto y Métricas
- **OKR Trimestral 1:**
  - *Objetivo:* Lanzar beta privada con experiencia de subasta completa.
  - *KR1:* 95% de subastas completadas sin incidentes.
  - *KR2:* Tiempo promedio de publicación < 60 segundos.
  - *KR3:* NPS beta ≥ 50.
- **OKR Trimestral 2:**
  - *Objetivo:* Escalar transacciones y monetización.
  - *KR1:* 30% de usuarios activos con ≥1 puja semanal.
  - *KR2:* 15% adopción de plan premium entre vendedores activos.
  - *KR3:* Tasa de disputas resueltas en <72h ≥ 90%.

### 17.1 Métricas Operativas
- Conversión publicación → primera puja (objetivo 70%).
- Tiempo promedio entre pujas (objetivo < 6 minutos en subastas activas).
- Valor recuperado por comisiones versus costos de pago.
- Tasa de fraude detectada versus fraude efectivo.

### 17.2 Analítica y Herramientas
- Implementación de eventos en Mixpanel/Amplitude.
- Dashboard en Looker Studio para equipo ejecutivo.
- Alertas automáticas ante caídas de pujas o tiempos de respuesta en chat.

## 18. Requerimientos Técnicos
### 18.1 Arquitectura de Alto Nivel
- Frontend móvil (Flutter/React Native) con soporte iOS y Android.
- Backend escalable (Node.js + NestJS o Django REST) desplegado en contenedores.
- Base de datos principal relacional (PostgreSQL) y caché en Redis para subastas.
- Servicio de mensajería en tiempo real (WebSockets) y colas (RabbitMQ/Kafka) para eventos críticos.

### 18.2 Integraciones Clave
- Proveedor de pagos con split escrow (ej. Culqi, Mercado Pago, Stripe).
- Servicios de geocodificación (Google Maps, Mapbox).
- Plataforma de notificaciones push (Firebase Cloud Messaging, OneSignal).
- Herramienta KYC/validación de identidad (ej. Truora, Incode).

### 18.3 Seguridad y Cumplimiento
- Cumplimiento PCI-DSS nivel SAQ A (tokenización de pagos).
- Cifrado de datos sensibles en reposo (AES-256) y en tránsito (TLS 1.2+).
- Política de contraseñas robusta con MFA opcional.
- Backups automáticos diarios y plan de recuperación ante desastres (RTO < 4h, RPO < 1h).

### 18.4 Escalabilidad
- Capacidad para soportar 5k subastas concurrentes con latencia < 200ms en actualizaciones de pujas.
- Autoescalado horizontal en infraestructura cloud (Kubernetes/Serverless).
- Monitorización con Prometheus + Grafana y alertas on-call.

## 19. Operaciones y Cumplimiento Legal
- Términos y condiciones claros, adaptados a legislación peruana y plan de expansión regional.
- Políticas de privacidad alineadas con normativa de protección de datos (Ley 29733 - Perú, LGPD Brasil).
- Registro contable de fondos en custodia y conciliaciones diarias.
- Mecanismo de reporte a autoridades ante actividades sospechosas.

## 20. Estrategia de Marketing y Comunidad
- Lanzamiento con campañas de influencers locales y microcreadores.
- Programa de referidos con recompensas escalonadas (saldo, destacados gratis).
- Contenido educativo (tutoriales, historias de éxito) en redes sociales.
- Eventos semanales “Subasta relámpago” con categorías temáticas.
- Comunidad en Discord/Telegram para feedback y soporte rápido.

## 21. Gestión de Riesgos
- **Riesgo:** fraude en pagos → *Mitigación:* proveedor antifraude + límites de transacción dinámicos.
- **Riesgo:** baja adopción inicial → *Mitigación:* alianzas estratégicas, incentivos a vendedores power-users.
- **Riesgo:** saturación de soporte → *Mitigación:* chatbot IA, base de conocimiento, escalamiento por niveles.
- **Riesgo:** problemas logísticos → *Mitigación:* múltiples partners, seguro opcional, monitoreo de SLA.

## 22. Roadmap Técnico (12 Meses)
1. **Q1:** MVP subastas 24h, pagos con custodia, chat básico, panel admin mínimo.
2. **Q2:** Gamificación, métricas avanzadas, logística integrada, versión web responsive.
3. **Q3:** IA de precios, verificación de tiendas, campañas masivas.
4. **Q4:** Subastas en vivo, moneda virtual, API partners.

## 23. Próximos Pasos Inmediatos
- Finalizar definición de historias de usuario y criterios de aceptación.
- Crear prototipo de alta fidelidad para pruebas con usuarios beta.
- Seleccionar proveedores de pago, KYC y logística.
- Establecer KPIs de soporte y crear playbooks de atención.

## 24. Historias de Usuario y Criterios de Aceptación (Ejemplos)
1. **Como vendedor quiero publicar un producto en menos de 60 segundos** para comenzar la subasta rápidamente.
   - *Dado* que estoy autenticado, *cuando* ingreso a “Publicar” y completo campos mínimos, *entonces* puedo enviar la subasta y ver un resumen de confirmación.
   - *Criterio:* tiempo promedio de publicación < 60s con conexión 4G.
2. **Como comprador quiero recibir alertas cuando superen mi puja** para poder reaccionar a tiempo.
   - *Dado* que tengo notificaciones activas, *cuando* otro usuario supere mi oferta, *entonces* recibo push y correo con el nuevo monto.
   - *Criterio:* notificación enviada < 5 segundos después del evento.
3. **Como administrador quiero revisar subastas reportadas** para garantizar seguridad.
   - *Dado* que accedo al panel, *cuando* filtro por “Reportadas”, *entonces* visualizo detalles, historial y puedo suspender o reinstaurar.
   - *Criterio:* decisión registrada en bitácora con timestamp y agente responsable.
