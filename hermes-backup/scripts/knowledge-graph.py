#!/usr/bin/env python3
"""
Grafo de conocimiento para Mastermind — versión final definitiva v3.
Solo usa frontmatter (tags + title). Sin body, sin ruido.
Umbral: 3+ tags/título compartidos.
"""
import os
import re
import json
from pathlib import Path
from collections import defaultdict

def extract_frontmatter_only(filepath):
    """Extraer keywords SOLO del frontmatter (tags + palabras del título)."""
    try:
        content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    except:
        return set(), set()
    
    stopwords = {
        "el", "la", "los", "las", "un", "una", "de", "del", "en", "con", "por",
        "para", "que", "es", "son", "se", "no", "y", "o", "a", "al", "como",
        "más", "este", "esta", "todo", "cada", "sin", "sobre", "pero", "sus",
        "su", "lo", "conmigo", "entre", "después", "antes", "desde", "hasta",
        "contra", "otro", "otra", "otros", "otras", "mismo", "misma", "también",
        "cuando", "donde", "muy", "puede", "tener", "hacer", "poder", "decir",
        "ir", "haber", "estar", "llegar", "pasar", "poner", "querer", "saber",
        "llevar", "parecer", "dejar", "creer", "quedar", "lleva", "cual", "casi",
        "tanto", "hoy", "ayer", "bien", "mal", "nunca", "siempre", "solo", "sido",
        "esos", "esas", "patron", "completo", "sistema", "uso", "usar",
        "funciona", "permite", "necesario", "ejemplo", "siguiente", "primer",
        "segundo", "ultimo", "tambien", "ademas", "además", "finalmente",
        "ademas", "sino", "aun", "aún", "incluso", "cualquier", "varios",
        "muchos", "algunos", "ningun", "ninguna", "algun", "alguna", "propio",
        "como", "usar", "patron", "sistema", "completo", "aprendizaje",
        "persistente", "sesion", "sesión", "dashboard", "frontend", "backend",
        "servidor", "cliente", "web", "api", "aplicacion", "aplicación",
        "codigo", "codigo", "archivo", "directorio", "carpeta", "ruta",
        "valor", "tipo", "dato", "informacion", "información", "contenido",
        "texto", "imagen", "video", "audio", "pagina", "navegador",
        "elemento", "funcion", "función", "variable", "lista", "array",
        "objeto", "json", "html", "css", "javascript", "python", "node",
        "npm", "git", "github", "docker", "terminal", "shell", "linux",
        "sistema", "operativo", "lectura", "escritura", "modo", "configuracion",
        "configuración", "opcion", "opcion", "parametro", "parámetro",
        "argumento", "entrada", "salida", "resultado", "error", "excepcion",
        "excepción", "log", "debug", "test", "prueba", "pruebas",
        "unitario", "integracion", "integración", "deploy", "despliegue",
        "build", "compilar", "compilador", "dependencia", "dependencias",
        "paquete", "libreria", "librería", "modulo", "modulo", "clase",
        "metodo", "metodo", "funcion", "función", "constante", "import",
        "export", "require", "resolve", "path", "url", "uri", "http",
        "https", "tcp", "udp", "websocket", "grpc", "rest", "graphql",
        "xml", "yaml", "toml", "csv", "msgpack", "protobuf", "gzip",
        "brotli", "zstd", "zip", "tar", "kubernetes", "k8s", "helm",
        "terraform", "ansible", "cloudformation", "serverless", "lambda",
        "fargate", "ecs", "eks", "gke", "aks", "azure", "aws", "gcp",
        "heroku", "vercel", "netlify", "railway", "fly", "render",
        "digitalocean", "monitoring", "logging", "tracing", "alerting",
        "grafana", "prometheus", "datadog", "newrelic", "sentry",
        "opentelemetry", "jaeger", "zipkin", "fluentd", "logstash",
        "kibana", "ci", "cd", "pipeline", "pipeline", "workflow", "accion",
        "acción", "github-actions", "gitlab", "jenkins", "circleci",
        "travis", "checkout", "release", "tag", "branch", "merge", "pull",
        "request", "issue", "commit", "push", "fetch", "clone", "fork",
        "star", "watch", "follow", "readme", "changelog", "license",
        "contributing", "security", "vulnerability", "cve", "dependabot",
        "snyk", "trivy", "grype", "audit", "review", "approve", "squash",
        "rebase", "cherry", "pick", "bisect", "blame", "diff", "status",
        "clean", "reset", "revert", "undo", "stash", "apply", "pop",
        "remote", "origin", "upstream", "downstream", "mirror", "submodule",
        "subtree", "sparse", "worktree", "reflog", "gc", "prune", "pack",
        "index", "stage", "unstaged", "untracked", "ignored", "gitignore",
        "gitattributes", "hooks", "pre-commit", "pre-push", "commit-msg",
        "post-commit", "post-merge", "post-checkout", "fsmonitor", "lfs",
        "large", "storage", "transfer", "filter", "smudge", "checkout",
        "merge", "conflict", "resolve", "ours", "theirs", "union", "rerere",
        "message", "template", "cleanup", "whitespace", "signoff", "gpg",
        "ssh", "pgp", "openpgp", "x509", "sks", "keyserver", "hkps", "hkp",
        "dns", "srvc", "txt", "a", "aaaa", "cname", "mx", "ns", "soa",
        "ptr", "spf", "dkim", "dmarc", "tls", "ssl", "cert", "certificate",
        "ca", "crl", "ocsp", "ct", "ctlog", "notary", "sigstore", "cosign",
        "rekor", "fulcio", "policy", "bundle", "transparency", "merkle",
        "tree", "proof", "verification", "signature", "sign", "verify",
        "hash", "sha256", "sha512", "blake2", "blake3", "md5", "crc32",
        "adler32", "xxhash", "siphash", "farmhash", "murmur", "cityhash",
        "spooky", "t1ha", "wyhash", "metrohash", "lookup3", "jshash",
        "rot13", "rot47", "base64", "base32", "base16", "base85", "utf8",
        "utf16", "utf32", "ascii", "latin1", "iso8859", "windows1252",
        "cp1252", "macroman", "gb2312", "gbk", "gb18030", "big5", "shiftjis",
        "eucjp", "euckr", "binary", "text", "null", "string", "byte", "char",
        "rune", "codepoint", "scalar", "grapheme", "cluster", "combining",
        "decomposition", "normalization", "nfc", "nfd", "nfkc", "canonical",
        "compatibility", "equivalence", "ordering", "collation", "sort",
        "locale", "collator", "comparator", "comparable", "hashable", "equal",
        "identical", "same", "reference", "value", "type", "duck", "structural",
        "nominal", "runtime", "compile", "static", "dynamic", "late", "early",
        "lazy", "eager", "immediate", "deferred", "scheduled", "queued",
        "batched", "streamed", "buffered", "unbuffered", "line", "block",
        "record", "frame", "packet", "segment", "datagram", "message",
        "event", "signal", "interrupt", "trap", "syscall", "ioctl", "mmap",
        "mprotect", "madvise", "mlock", "munlock", "mlockall", "munlockall",
        "mremap", "munmap", "brk", "sbrk", "madvise", "mlock", "munlock",
        "mlockall", "munlockall", "mremap", "mprotect", "madvise", "mlock",
        "munlock", "mlockall", "munlockall", "mremap",
        "todo", "feature", "bugfix", "fix", "improve", "update", "change",
        "modify", "add", "remove", "delete", "create", "new", "old",
        "first", "last", "next", "previous", "current", "main", "master",
        "develop", "staging", "production", "prod", "dev", "test", "qa",
        "live", "alpha", "beta", "rc", "release", "version", "major",
        "minor", "patch", "semver", "breaking", "deprecated", "obsolete",
        "legacy", "modern", "upcoming", "planned", "future", "past",
        "present", "active", "inactive", "enabled", "disabled", "on", "off",
        "yes", "no", "true", "false", "ok", "warning", "info", "debug",
        "trace", "verbose", "quiet", "silent", "loud", "fast", "slow",
        "quick", "rapid", "instant", "delayed", "immediate", "scheduled",
        "periodic", "continuous", "batch", "realtime", "real-time",
        "near-realtime", "async", "synchronous", "asynchronous", "parallel",
        "sequential", "concurrent", "serial", "distributed", "centralized",
        "decentralized", "peer", "proxy", "gateway", "edge", "core",
        "middle", "front", "back", "top", "bottom", "left", "right",
        "center", "inner", "outer", "internal", "external", "public",
        "private", "protected", "restricted", "open", "closed", "locked",
        "unlocked", "read", "write", "execute", "append", "truncate",
        "delete", "rename", "move", "copy", "link", "symlink", "hardlink",
        "junction", "mount", "unmount", "attach", "detach", "bind",
        "unbind", "map", "unmap", "lock", "unlock", "acquire", "release",
        "obtain", "free", "allocate", "deallocate", "malloc", "calloc",
        "realloc", "new", "delete", "construct", "destruct", "init",
        "deinit", "setup", "teardown", "bootstrap", "initialize",
        "finalize", "cleanup", "dispose", "close", "open", "start",
        "stop", "pause", "resume", "restart", "reload", "refresh",
        "update", "upgrade", "downgrade", "install", "uninstall", "remove",
        "add", "insert", "append", "prepend", "push", "pop", "shift",
        "unshift", "splice", "slice", "concat", "join", "split", "merge",
        "flatten", "map", "filter", "reduce", "fold", "scan", "transform",
        "convert", "parse", "serialize", "deserialize", "encode", "decode",
        "compress", "decompress", "encrypt", "decrypt", "sign", "verify",
        "hash", "digest", "checksum", "validate", "sanitize", "escape",
        "unescape", "normalize", "denormalize", "format", "tokenize", "lex",
        "ast", "tree", "graph", "network", "forest", "heap", "stack",
        "queue", "deque", "priority", "set", "map", "dict", "table",
        "array", "list", "vector", "buffer", "ring", "circular", "bounded",
        "unbounded", "fixed", "dynamic", "static", "constant", "variable",
        "mutable", "immutable", "read", "write", "readwrite", "readonly",
        "read-only", "get", "set", "put", "post", "patch", "delete",
        "head", "options", "trace", "connect", "fetch", "load", "save",
        "store", "cache", "evict", "flush", "invalidate", "warm", "cool",
        "hot", "cold", "hotpath", "coldpath", "fastpath", "slowpath",
        "error", "path", "success", "fallback", "retry", "timeout",
        "deadline", "circuit", "breaker", "rate", "limit", "throttle",
        "backpressure", "flow", "control", "backoff", "exponential",
        "linear", "fixed", "jitter", "random", "deterministic", "stochastic",
        "probabilistic", "nondeterministic", "pseudo", "seed", "rng", "prng",
        "drbg", "csp_rng", "cryptographic", "secure", "insecure", "safe",
        "unsafe", "trusted", "untrusted", "authenticated", "authorized",
        "permission", "privilege", "role", "group", "user", "admin",
        "superuser", "root", "sudo", "su", "runas", "setuid", "setgid",
        "capabilities", "seccomp", "selinux", "apparmor", "namespace",
        "cgroup", "container", "sandbox", "jail", "chroot", "pivot",
        "overlay", "union", "merge", "diff", "patch", "delta", "incremental",
        "full", "backup", "restore", "snapshot", "checkpoint", "recovery",
        "failover", "failback", "drain", "scale", "up", "down", "out", "in",
        "auto", "manual", "automatic", "scheduled", "on-demand",
        "event-driven", "request-response", "pub-sub", "stream", "batch",
        "real-time", "near-real-time", "offline", "online", "connected",
        "disconnected", "available", "unavailable", "reachable",
        "unreachable",
    }
    
    # Extraer frontmatter
    fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    fm_text = fm_match.group(1) if fm_match else ""
    
    # Extraer tags
    tags = set()
    tags_match = re.search(r'tags:\s*\[(.+?)\]', fm_text)
    if tags_match:
        for tag in tags_match.group(1).split(','):
            tag = tag.strip().strip('"').strip("'")
            if tag:
                tags.add(tag.lower())
    
    # Extraer título y palabras clave del título
    title_match = re.search(r'title:\s*(.+)', fm_text)
    title = title_match.group(1).strip() if title_match else ""
    
    # Extraer category
    cat_match = re.search(r'category:\s*(.+)', fm_text)
    category = cat_match.group(1).strip().lower() if cat_match else ""
    
    # Palabras del título (sin stopwords)
    title_words = set()
    for word in re.findall(r'\b[a-záéíóúüñ]{4,}\b', title.lower()):
        if word not in stopwords:
            title_words.add(word)
    
    # Keywords = tags + title_words (sin body)
    keywords = tags | title_words
    
    # Extraer referencias a otros skills
    skill_refs = set()
    for match in re.finditer(r"(?:skill|skills?)[\s:]+([a-z0-9_-]+)", content, re.IGNORECASE):
        skill_refs.add(match.group(1).lower())
    for match in re.finditer(r"name=['\"]([a-z0-9_-]+)['\"]", content):
        skill_refs.add(match.group(1).lower())
    for match in re.finditer(r'`([a-z0-9_-]+)`', content):
        skill_refs.add(match.group(1).lower())
    
    return keywords, skill_refs

def build_graph(skills_dir, notes_dir):
    """Construir grafo de conexiones."""
    nodes = {}
    edges = defaultdict(list)
    
    print("📚 Indexando skills...")
    for skill_md in Path(skills_dir).rglob("SKILL.md"):
        skill_name = skill_md.parent.name
        keywords, refs = extract_frontmatter_only(skill_md)
        nodes[skill_name] = {
            "type": "skill",
            "path": str(skill_md),
            "keywords": keywords,
            "refs": refs
        }
    
    print("📝 Indexando notas...")
    for md_file in Path(notes_dir).glob("*.md"):
        if md_file.name.startswith(".") or md_file.name == "_template.md":
            continue
        note_name = md_file.stem
        keywords, refs = extract_frontmatter_only(md_file)
        nodes[note_name] = {
            "type": "note",
            "path": str(md_file),
            "keywords": keywords,
            "refs": refs
        }
    
    skill_count = len([n for n in nodes.values() if n["type"] == "skill"])
    note_count = len([n for n in nodes.values() if n["type"] == "note"])
    print(f"  Nodos: {len(nodes)} ({skill_count} skills, {note_count} notas)")
    
    # Mostrar distribución de keywords
    kw_counts = [(n, len(d["keywords"])) for n, d in nodes.items()]
    kw_counts.sort(key=lambda x: x[1], reverse=True)
    print(f"\n  Top 10 nodos por keywords:")
    for name, count in kw_counts[:10]:
        print(f"    {name}: {count} keywords")
    
    # Detectar conexiones
    print("\n🔗 Detectando conexiones...")
    node_names = list(nodes.keys())
    
    for i, name_a in enumerate(node_names):
        node_a = nodes[name_a]
        
        for name_b in node_names[i+1:]:
            node_b = nodes[name_b]
            
            shared_keywords = node_a["keywords"] & node_b["keywords"]
            if len(shared_keywords) >= 3:
                edges[name_a].append({
                    "target": name_b,
                    "type": "keyword_overlap",
                    "strength": len(shared_keywords),
                    "shared": list(shared_keywords)[:5]
                })
        
        for ref in node_a["refs"]:
            if ref in nodes and ref != name_a:
                existing_targets = [e["target"] for e in edges[name_a]]
                if ref not in existing_targets:
                    edges[name_a].append({
                        "target": ref,
                        "type": "direct_reference",
                        "strength": 10
                    })
    
    # Detectar skills huérfanas
    connected_nodes = set()
    for src, targets in edges.items():
        connected_nodes.add(src)
        for t in targets:
            connected_nodes.add(t["target"])
    
    orphans = [name for name, data in nodes.items() 
               if data["type"] == "skill" and name not in connected_nodes]
    
    clusters = defaultdict(list)
    for name, edge_list in edges.items():
        if len(edge_list) >= 3:
            clusters[name] = [e["target"] for e in edge_list[:5]]
    
    return nodes, dict(edges), orphans, dict(clusters)

def main():
    skills_dir = "/hermes-home/skills"
    notes_dir = "/root/workspace/Mastermind/notes"
    output_dir = "/root/workspace/Mastermind/learning"
    
    os.makedirs(output_dir, exist_ok=True)
    
    nodes, edges, orphans, clusters = build_graph(skills_dir, notes_dir)
    
    report = {
        "generated": "2026-06-10",
        "stats": {
            "total_nodes": len(nodes),
            "skills": len([n for n in nodes.values() if n["type"] == "skill"]),
            "notes": len([n for n in nodes.values() if n["type"] == "note"]),
            "total_edges": sum(len(v) for v in edges.values()),
            "orphans": len(orphans),
            "clusters": len(clusters)
        },
        "orphan_skills": orphans,
        "clusters": clusters,
        "top_connected": sorted(edges.keys(), key=lambda x: len(edges[x]), reverse=True)[:15]
    }
    
    with open(os.path.join(output_dir, "knowledge-graph.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Generar Markdown
    md = f"""# 🕸️ Grafo de Conocimiento de Mastermind
Generado: {report['generated']}

## Estadísticas
- **Nodos totales:** {report['stats']['total_nodes']}
- **Skills:** {report['stats']['skills']}
- **Notas:** {report['stats']['notes']}
- **Conexiones:** {report['stats']['total_edges']}
- **Skills huérfanas:** {report['stats']['orphans']}
- **Clusters detectados:** {report['stats']['clusters']}

## 🔗 Nodos más conectados
"""
    for name in report["top_connected"]:
        count = len(edges[name])
        node_type = nodes[name]["type"]
        md += f"- **{name}** ({node_type}) → {count} conexiones\n"
    
    if orphans:
        md += f"\n## ⚠️ Skills Huérfanas (sin conexiones)\n"
        for o in orphans[:20]:
            md += f"- `{o}`\n"
    else:
        md += "\n## ✅ No hay skills huérfanas\n"
    
    if clusters:
        md += f"\n## 🏘️ Clusters de Conocimiento\n"
        for center, members in list(clusters.items())[:5]:
            md += f"\n**{center}** → {', '.join(members[:3])}\n"
    
    with open(os.path.join(output_dir, "knowledge-graph.md"), "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"\n📊 RESUMEN:")
    print(f"  Nodos: {report['stats']['total_nodes']}")
    print(f"  Conexiones: {report['stats']['total_edges']}")
    print(f"  Huérfanas: {report['stats']['orphans']}")
    print(f"  Clusters: {report['stats']['clusters']}")
    print(f"\n  Top 5 conectados:")
    for name in report["top_connected"][:5]:
        print(f"    {name}: {len(edges[name])}")

if __name__ == "__main__":
    main()
