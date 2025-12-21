"""
Estilos CSS personalizados para la interfaz.
Diseño profesional y moderno.
"""

# Estilos CSS personalizados
CUSTOM_CSS = """
<style>
/* ==================== VARIABLES Y TEMA ==================== */
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    --dark-gradient: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    
    --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 25px rgba(0,0,0,0.15);
    --shadow-xl: 0 20px 40px rgba(0,0,0,0.2);
    
    --border-radius: 12px;
    --border-radius-lg: 16px;
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ==================== ANIMACIONES ==================== */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { transform: translateX(-20px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* ==================== CARDS Y CONTENEDORES ==================== */
.q-card {
    border-radius: var(--border-radius) !important;
    box-shadow: var(--shadow-md) !important;
    transition: var(--transition) !important;
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.98) !important;
    border: 1px solid rgba(0,0,0,0.05);
}

.q-card:hover {
    box-shadow: var(--shadow-lg) !important;
    transform: translateY(-2px);
}

/* Tarjetas con gradiente */
.gradient-card {
    background: var(--primary-gradient) !important;
    color: white !important;
}

.gradient-card-success {
    background: var(--success-gradient) !important;
    color: white !important;
}

.gradient-card-warning {
    background: var(--warning-gradient) !important;
    color: white !important;
}

/* ==================== HEADER ==================== */
header.q-header {
    background: var(--dark-gradient) !important;
    box-shadow: var(--shadow-lg) !important;
    backdrop-filter: blur(20px);
}

/* ==================== BOTONES ==================== */
.q-btn {
    border-radius: 10px !important;
    font-weight: 600 !important;
    text-transform: none !important;
    letter-spacing: 0.5px !important;
    transition: var(--transition) !important;
    box-shadow: var(--shadow-sm) !important;
}

.q-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md) !important;
}

.q-btn:active:not(:disabled) {
    transform: translateY(0);
}

/* Botón de emergencia con efecto pulsante */
.q-btn.emergency-btn {
    animation: pulse 2s infinite;
    box-shadow: 0 0 20px rgba(193, 0, 21, 0.5) !important;
}

.q-btn.emergency-btn:hover {
    animation: none;
    box-shadow: 0 0 30px rgba(193, 0, 21, 0.8) !important;
}

/* Botones con gradiente */
.btn-gradient-primary {
    background: var(--primary-gradient) !important;
    border: none !important;
    color: white !important;
}

.btn-gradient-success {
    background: var(--success-gradient) !important;
    border: none !important;
    color: white !important;
}

/* ==================== PROGRESS BAR ==================== */
.q-linear-progress {
    border-radius: 10px !important;
    overflow: hidden !important;
    background: rgba(0,0,0,0.05) !important;
}

.q-linear-progress__track {
    background: var(--primary-gradient) !important;
    transition: width 0.5s ease !important;
}

/* Progress bar animado */
.q-linear-progress.animated .q-linear-progress__track {
    background: linear-gradient(
        90deg,
        #667eea 0%,
        #764ba2 50%,
        #667eea 100%
    ) !important;
    background-size: 200% 100% !important;
    animation: shimmer 2s linear infinite !important;
}

/* ==================== BADGES ==================== */
.q-badge {
    border-radius: 8px !important;
    padding: 6px 12px !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ==================== INPUTS Y SELECTS ==================== */
.q-field {
    border-radius: 10px !important;
}

.q-field__control {
    border-radius: 10px !important;
    background: rgba(0,0,0,0.02) !important;
    transition: var(--transition) !important;
}

.q-field__control:hover {
    background: rgba(0,0,0,0.04) !important;
}

.q-field--focused .q-field__control {
    background: white !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* ==================== TABS ==================== */
.q-tabs {
    border-radius: var(--border-radius) !important;
    background: rgba(255,255,255,0.8) !important;
    backdrop-filter: blur(10px);
    box-shadow: var(--shadow-sm) !important;
}

.q-tab {
    border-radius: 8px !important;
    margin: 4px !important;
    transition: var(--transition) !important;
}

.q-tab:hover {
    background: rgba(102, 126, 234, 0.1) !important;
}

.q-tab--active {
    background: var(--primary-gradient) !important;
    color: white !important;
    box-shadow: var(--shadow-md) !important;
}

/* ==================== SEPARADORES ==================== */
.q-separator {
    background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(0,0,0,0.1) 50%,
        transparent 100%
    ) !important;
    height: 1px !important;
}

/* ==================== ICONOS ==================== */
.q-icon {
    transition: var(--transition) !important;
}

.q-icon.rotating {
    animation: rotate 2s linear infinite;
}

/* Iconos con efecto hover */
.icon-hover:hover .q-icon {
    transform: scale(1.2);
    filter: drop-shadow(0 0 8px currentColor);
}

/* ==================== DIALOGS ==================== */
.q-dialog__backdrop {
    backdrop-filter: blur(8px) !important;
    background: rgba(0,0,0,0.5) !important;
}

.q-dialog .q-card {
    animation: fadeIn 0.3s ease-out;
    max-height: 90vh !important;
    overflow: auto !important;
}

/* ==================== SCROLLBAR PERSONALIZADA ==================== */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(0,0,0,0.05);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: var(--primary-gradient);
    border-radius: 10px;
    border: 2px solid transparent;
    background-clip: padding-box;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--dark-gradient);
    background-clip: padding-box;
}

/* ==================== TARJETAS DE OPERACIÓN ==================== */
.operation-card {
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.operation-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255,255,255,0.3),
        transparent
    );
    transition: left 0.5s;
}

.operation-card:hover::before {
    left: 100%;
}

.operation-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: var(--shadow-xl) !important;
}

/* ==================== TARJETAS DE RECETA ==================== */
.recipe-card {
    position: relative;
    overflow: hidden;
    border: 2px solid transparent;
    transition: var(--transition) !important;
}

.recipe-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: var(--border-radius);
    padding: 2px;
    background: var(--primary-gradient);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    opacity: 0;
    transition: var(--transition);
}

.recipe-card:hover::after {
    opacity: 1;
}

/* ==================== INDICADORES DE ESTADO ==================== */
.status-indicator {
    position: relative;
}

.status-indicator.active::before {
    content: '';
    position: absolute;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #21BA45;
    box-shadow: 0 0 10px #21BA45;
    animation: pulse 2s infinite;
}

/* ==================== GLASS MORPHISM ==================== */
.glass {
    background: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1) !important;
}

.glass-dark {
    background: rgba(30, 41, 59, 0.7) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    color: white !important;
}

/* ==================== FOOTER ==================== */
footer.q-footer {
    background: var(--dark-gradient) !important;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.1) !important;
}

/* ==================== EFECTOS DE CARGA ==================== */
.loading {
    position: relative;
    overflow: hidden;
}

.loading::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.3),
        transparent
    );
    animation: shimmer 2s infinite;
}

/* ==================== GRID RESPONSIVO ==================== */
@media (max-width: 768px) {
    .q-card {
        margin: 8px !important;
    }
    
    .operation-card {
        margin: 4px !important;
    }
}

/* ==================== UTILIDADES ==================== */
.hover-lift {
    transition: var(--transition) !important;
}

.hover-lift:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg) !important;
}

.text-gradient {
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.border-gradient {
    border: 2px solid transparent;
    background: linear-gradient(white, white) padding-box,
                var(--primary-gradient) border-box;
    border-radius: var(--border-radius);
}

/* ==================== ANIMACIÓN DE ENTRADA ==================== */
.fade-in {
    animation: fadeIn 0.5s ease-out;
}

.slide-in {
    animation: slideIn 0.5s ease-out;
}

/* ==================== ESTADOS DE BOTÓN ==================== */
.q-btn:disabled {
    opacity: 0.5 !important;
    cursor: not-allowed !important;
    transform: none !important;
}

/* ==================== NOTIFICACIONES ==================== */
.q-notification {
    border-radius: var(--border-radius) !important;
    box-shadow: var(--shadow-lg) !important;
    backdrop-filter: blur(10px);
}

/* ==================== TOOLTIPS ==================== */
.q-tooltip {
    background: rgba(0, 0, 0, 0.9) !important;
    backdrop-filter: blur(10px);
    border-radius: 8px !important;
    font-size: 12px !important;
    padding: 8px 12px !important;
    box-shadow: var(--shadow-md) !important;
}
</style>
"""

def inject_custom_styles():
    """Inyecta los estilos personalizados en la página."""
    from nicegui import ui
    ui.add_head_html(CUSTOM_CSS)