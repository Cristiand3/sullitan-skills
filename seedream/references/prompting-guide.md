# Guía de Prompting — SeedREAM 5.0

## Principios clave

1. **Lenguaje natural, no keywords.** "Una chica con vestido elegante caminando bajo un paraguas por un camino arbolado, estilo pintura de Monet" funciona mejor que "chica, paraguas, calle arbolada, textura pintura al óleo."
2. **Texto entre comillas dobles.** Si querés texto en la imagen, poné entre comillas dobles: `"SulliTan.ia"`
3. **Sé específico con lo que debe mantenerse** al editar: "Reemplazá el sombrero por una corona, manteniendo la pose y expresión."
4. **Para edición por ejemplo, mostrá en vez de describir.** Cuando la transformación es difícil de poner en palabras, usá pares antes/después.
5. **Especificá el caso de uso.** "Diseñá un logo para una empresa de gaming" da mejores resultados que solo describir los elementos visuales.

## Capacidades principales

### Generación texto a imagen
- Entiende lenguaje fotográfico: film stocks, lentes, iluminación
- Calidad estética excepcional — detalles que se mantienen al hacer zoom
- Seguimiento preciso de instrucciones: colores, cantidades, relaciones espaciales

### Edición basada en ejemplos (multi-imagen)
- Dar par antes/después (Imagen 1 y 2) + Imagen 3 → aplica la misma transformación
- Prompt: "Reference the change from Image 1 to Image 2, apply the same operation to Image 3"
- Usos: cambio de material, cambio de escena, transferencia de estilo

### Razonamiento lógico
- Entiende relaciones físicas, procesos, mecánica
- Puede razonar sobre pasos múltiples con imágenes de entrada
- Ejemplo: clasificar flores por tipo y distribuirlas en jarrones

### Conocimiento de dominio
- Arquitectura: de boceto a render fotorrealista
- Ciencia: ilustraciones con etiquetas precisas
- Diseño: composiciones profesionales

### Generación por lotes
- Sets relacionados: storyboards, identidad de marca, hojas de personaje

## Ejemplos de prompts efectivos

### Retrato cinematográfico
```
A color film-inspired portrait of a young man looking to the side with a shallow depth of field that blurs the surrounding elements. The fine grain suggests high ISO film stock, while the wide aperture lens creates a motion blur effect, enhancing the candid documentary style.
```

### Escena urbana con grading específico
```
A woman standing in a Tokyo alleyway at dusk, neon signs reflecting off wet pavement. Shot on expired Kodak Portra 800, pushed two stops. The tungsten light from a ramen shop spills warm orange across her face while the neon casts cool cyan highlights on her hair. Visible grain, halation around the light sources, slightly lifted blacks.
```

### Producto publicitario con detalles precisos
```
A photorealistic cluttered office desk. An open MacBook Pro displays a terminal with green-on-black code. A ceramic mug reads "console.log('coffee')" in monospace font, steam curling up. Golden hour light rakes across from the right, casting long shadows.
```

### Edición por ejemplo
```
Reference the change from Image 1 to Image 2, apply the same operation to Image 3
```

### Transformación de estilo
```
Reimagine this scene as a traditional Japanese Ukiyo-e woodblock print — flat perspective, bold outlines, limited color palette of indigo, vermillion, and ochre.
```

### Con marcadores visuales
```
Furnish this loft according to the spray-painted markers. Place a large abstract painting where the red rectangle is. Place a mid-century sofa where the blue rectangle is. Hang a brass pendant light where the yellow circle is. Remove the markers. Keep the industrial character.
```

## Resoluciones y formatos
- **2K**: hasta 2048px
- **3K**: hasta 3072px
- Ratios: 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9
- Formatos: PNG, JPG
