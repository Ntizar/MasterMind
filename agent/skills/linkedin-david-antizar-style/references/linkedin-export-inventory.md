# LinkedIn Export File Inventory (2026-06-05)

## Contexto
Export completo de LinkedIn de David Antizar. 29 CSVs + 4 HTMLs.

## CSVs (29)

### Perfil y datos básicos
- **Profile.csv** — First Name, Last Name, Headline, Summary, Industry, Geo Location, Websites
- **Profile_Summary.csv** — Profile Summary (vacío en este export)
- **Registration.csv** — Registered At, Registration IP, Subscription Types
- **Email_Addresses.csv** — Email Address, Confirmed, Primary, Updated On
- **PhoneNumbers.csv** — Extension, Number, Type

### Experiencia
- **Positions.csv** — Company Name, Title, Description, Location, Started On, Finished On (14 posiciones)

### Educación
- **Education.csv** — School Name, Start Date, End Date, Notes, Degree Name, Activities

### Skills
- **Skills.csv** — Name (53 skills)
- **Endorsement_Given_Info.csv** — Endorsement Date, Skill Name, Endorsee First/Last Name, Status (27)
- **Endorsement_Received_Info.csv** — Endorsement Date, Skill Name, Endorser First/Last Name, Status (71)

### Certificaciones
- **Certifications.csv** — Name, Url, Authority, Started On, Finished On, License Number

### Publicaciones
- **Publications.csv** — Name, Published On, Description, Publisher, Url

### Honores y logros
- **Honors.csv** — Title, Description, Issued On

### Voluntariado
- **Volunteering.csv** — Company Name, Role, Cause, Started On, Finished On, Description

### Idiomas
- **Languages.csv** — Name, Proficiency

### Intereses
- **Causes_You_Care_About.csv** — Supported Cause (4)
- **Company_Follows.csv** — Organization, Followed On (440 empresas)

### Conexiones
- **Connections.csv** — First Name, Last Name, URL, Email Address, Company, Position, Connected On (3086 conexiones)
- **Invitations.csv** — From, To, Sent At, Message, Direction (563)

### Mensajes
- **messages.csv** — Conversation ID, Title, From, To, Date, Subject, Content, Attachments (6486 mensajes)
- **guide_messages.csv** — Conversations con LinkedIn guides (0)
- **learning_coach_messages.csv** — Coach messages (0)
- **learning_role_play_messages.csv** — Role play messages (0)

### Aprendizaje
- **Learning.csv** — Content Title, Description, Type, Last Watched, Completed, Notes (557 cursos)

### Eventos
- **Events.csv** — Event Name, Event Time, Status, External Url (61)

### Rich Media
- **Rich_Media.csv** — Date/Time, Media Description, Media Link (120 uploads)

### Búsqueda de empleo
- **SavedJobAlerts.csv** — Alert Parameters, Query Context, Search ID
- **Job_Applicant_Saved_Screening_Question_Responses.csv** — Question, Answer (38)

### Targeting (datos que LinkedIn tiene sobre ti)
- **Ad_Targeting.csv** — Member Age, Buyer Groups, Company Names, Company Size, Degrees, Devices, Schools, Job Functions, Member Gender, Graduation Year, Member Groups, Job Seniorities, Member Skills, Standard Audience Segments, Job Titles, Profile Locations, Company Revenue, Years of Experience

## HTMLs (4 artículos publicados)

1. **adapaes-la-reforma-sin-preocupaciones-david-antizar.html** — 2020-05-29, plataforma de presupuestos de reforma
2. **comparativa-entre-instalaciones-térmicas-de-gas-natural-david-antizar.html** — 2021-02-11, gas natural vs biomasa
3. **el-real-decreto-3902021-y-la-segunda-oportunidad-para-david-antizar.html** — 2021-06-29, certificado energético
4. **world-energy-outlook-2022-i-david-antizar.html** — 2022-10-27, informe AIE

## Análisis rápido de estilo (de los 4 artículos)

| Métrica | Valor |
|---------|-------|
| Párrafos | 8-32 por artículo |
| Longitud media párrafo | 130-236 chars |
| Frases cortas (<80 chars) | 7-17 |
| Números mencionados | 10-58 |
| Emojis | 0 |
| Citas | 0-1 |

## Notas importantes

- **NUNCA guardar credenciales** de LinkedIn en ningún archivo
- LinkedIn bloquea scraping automatizado — solo via export oficial
- Los HTMLs usan formato Slate/Journalism — limpiar con regex para extraer texto
- Los CSVs pueden tener campos vacíos — verificar antes de analizar
- Ad_Targeting.csv contiene datos que LinkedIn inferió sobre el perfil (edad, intereses, segmentos)
