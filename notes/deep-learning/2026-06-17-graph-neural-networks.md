# Graph Neural Networks (GNNs) — Aprendizaje sobre Grafos

**Fecha:** 2026-06-17  
**Tema:** 6 de la serie deep-learning-fundamentals  
**Autor:** Mastermind (David Antizar)

---

## 1. ¿Qué son las GNNs?

Las **Graph Neural Networks** son redes neuronales diseñadas para operar sobre datos estructurados como grafos. A diferencia de CNNs (datos en rejilla) o Transformers (secuencias), las GNNs operan sobre estructuras de grafos arbitrarios: nodos, aristas y sus características.

**Aplicaciones directas al stack ESIOS:**
- **Red eléctrica española** = grafo natural (subestaciones = nodos, líneas = aristas)
- **Redes de transporte GTFS** = grafos bipartitos (paradas ↔ rutas)
- **Datos satelitales** = grafos de proximidad espacial
- **Redes de sensores** = grafos dinámicos con topología variable

---

## 2. Fundamentos Teóricos

### 2.1 Message Passing Framework

El paradigma unificador de todas las GNNs es el **Message Passing Neural Network (MPNN)** de Gilmer et al. (2017):

```
Para cada paso de mensaje t = 1, ..., T:
    1. MESSAGE:    m_ij^t = M^t(h_i^t, h_j^t, e_ij)
    2. AGGREGATE:  m_i^t = Σ_{j∈N(i)} m_ij^t
    3. UPDATE:     h_i^{t+1} = U^t(h_i^t, m_i^t)
    4. PREDICT:    ŷ_i = φ(h_i^{T+1})
```

Donde:
- `h_i^t` = embedding del nodo i en el paso t
- `e_ij` = características de la arista (i,j)
- `N(i)` = vecinos de i
- `M^t`, `U^t`, `φ` = funciones diferenciables (MLPs)

### 2.2 ¿Por qué no usar Transformers normales?

Los Transformers asumen datos con estructura de rejilla o secuencia. Los grafos tienen:
- **Topología variable** entre instancias
- **Invariancia permutacional** (el orden de nodos no importa)
- **Grados desbalanceados** (algunos nodos tienen 2 vecinos, otros 2000)

Las GNNs resuelven esto con message passing sobre la estructura real del grafo.

---

## 3. Arquitecturas Principales

### 3.1 GCN — Graph Convolutional Network

**Paper:** Kipf & Welling, "Semi-Supervised Classification with GCNs" (ICLR 2017)

La GCN hace una aproximación de primer orden del Laplacian espectral:

```
H^{(l+1)} = σ(D̂^{-1/2} Ã D̂^{-1/2} H^{(l)} W^{(l)})
```

Donde:
- `Ã = A + I` = adyacencia con self-loops
- `D̂` = grado diagonal de Ã
- `D̂^{-1/2} Ã D̂^{-1/2}` = matriz de adyacencia normalizada simétrica

**Ventaja:** 1-hop, muy eficiente. **Desventaja:** over-smoothing con muchas capas.

### 3.2 GraphSAGE

**Paper:** Hamilton et al., "Inductive Representation Learning on Large Graphs" (NeurIPS 2017)

En lugar de usar toda la matriz de adyacencia (como GCN), GraphSAGE:
1. **Muestrea vecinos** de tamaño fijo por nodo
2. **Agrega** con funciones learnable (mean, LSTM, pooling)

```
h_i^{(l+1)} = σ(W^{(l)} · CONCAT(h_i^{(l)}, AVG({h_j^{(l)} : j ∈ N(i)})))
```

**Ventaja:** inductivo (nodos no vistos), escalable a grafos grandes.

### 3.3 GAT — Graph Attention Network

**Paper:** Veličković et al., "Graph Attention Networks" (ICLR 2018)

Usa mecanismos de atención para ponderar la importancia de cada vecino:

```
α_ij = softmax_j(LeakyReLU(a^T [W h_i || W h_j]))
h_i' = σ(Σ_j α_ij W h_j)
```

**Ventaja:** aprende qué vecinos son importantes. **Desventaja:** O(n²) en atención densa.

### 3.4 GCN vs GraphSAGE vs GAT — Comparativa

| Característica | GCN | GraphSAGE | GAT |
|---|---|---|---|
| Tipo | Transductivo | Inductivo | Inductivo |
| Escalabilidad | O(n²) | O(n·k) | O(n·k·heads) |
| Capas prácticas | 2-3 | 2-5 | 2-4 |
| Over-smoothing | Alto | Medio | Medio |
| Parámetros | Bajos | Medios | Altos |
| Mejor para | Grafos pequeños | Grafos grandes | Topologías heterogéneas |

---

## 4. Implementación Práctica con PyTorch Geometric

### 4.1 Instalación

```bash
pip install torch torch-geometric
# O con CUDA:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install torch-geometric
```

### 4.2 GCN desde cero

```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data

class GCN(torch.nn.Module):
    """GCN de 2 capas para node classification."""
    
    def __init__(self, num_features, num_classes, hidden_dim=16, dropout=0.5):
        super().__init__()
        self.conv1 = GCNConv(num_features, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, num_classes)
        self.dropout = dropout
    
    def forward(self, x, edge_index, edge_attr=None):
        """
        Args:
            x: (num_nodes, num_features) - características de nodos
            edge_index: (2, num_edges) - COO format [source, target]
            edge_attr: (num_edges, num_edge_features) - características de aristas (opcional)
        Returns:
            logits: (num_nodes, num_classes)
        """
        # Primera capa GCN
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=self.dropout, training=self.training)
        
        # Segunda capa GCN
        x = self.conv2(x, edge_index)
        
        return F.log_softmax(x, dim=1)


# === Ejemplo de uso ===
# Crear un grafo synthetic: 100 nodos, 500 aristas
num_nodes = 100
num_features = 16
num_classes = 4

# Características de nodos
x = torch.randn(num_nodes, num_features)

# Aristas aleatorias (COO format)
edge_index = torch.randint(0, num_nodes, (2, 500))
# Asegurar simetría
edge_index = torch.cat([edge_index, edge_index.flip(0)], dim=1).unique(dim=1)

# Labels
y = torch.randint(0, num_classes, (num_nodes,))

# Crear grafo
data = Data(x=x, edge_index=edge_index, y=y)

# Modelo
model = GCN(num_features, num_classes, hidden_dim=32)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

# Training
model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(x, edge_index)
    loss = F.nll_loss(out, y)
    loss.backward()
    optimizer.step()
    
    if epoch % 50 == 0:
        print(f"Epoch {epoch}: loss = {loss.item():.4f}")

# Inference
model.eval()
with torch.no_grad():
    logits = model(x, edge_index)
    predictions = logits.argmax(dim=1)
```

### 4.3 GAT con atención multi-head

```python
from torch_geometric.nn import GATConv

class GAT(torch.nn.Module):
    """GAT con attention multi-head."""
    
    def __init__(self, num_features, num_classes, hidden_dim=8, 
                 num_heads=4, dropout=0.6):
        super().__init__()
        # Primera capa: multi-head attention
        self.conv1 = GATConv(
            num_features, hidden_dim, 
            heads=num_heads,           # 4 heads paralelos
            dropout=dropout,
            concat=True                # concatena outputs de heads
        )
        # Segunda capa: single head (promedia)
        self.conv2 = GATConv(
            hidden_dim * num_heads, num_classes,
            heads=1,                   # single head
            concat=False,              # promedia outputs
            dropout=dropout
        )
        self.dropout = dropout
    
    def forward(self, x, edge_index):
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.conv1(x, edge_index)
        x = F.elu(x)
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)
```

### 4.4 GraphSAGE para grafos grandes

```python
from torch_geometric.nn import SAGNEncoder, SAGEConv

class GraphSAGE(torch.nn.Module):
    """GraphSAGE para node classification inductivo."""
    
    def __init__(self, num_features, num_classes, hidden_dim=64, 
                 num_layers=3, dropout=0.5):
        super().__init__()
        self.convs = torch.nn.ModuleList()
        self.bns = torch.nn.ModuleList()
        
        # Primera capa
        self.convs.append(SAGEConv(num_features, hidden_dim))
        self.bns.append(torch.nn.BatchNorm1d(hidden_dim))
        
        # Capas intermedias
        for _ in range(num_layers - 2):
            self.convs.append(SAGEConv(hidden_dim, hidden_dim))
            self.bns.append(torch.nn.BatchNorm1d(hidden_dim))
        
        # Última capa
        self.convs.append(SAGEConv(hidden_dim, num_classes))
    
    def forward(self, x, edge_index):
        for i, conv in enumerate(self.convs):
            x = conv(x, edge_index)
            if i < len(self.convs) - 1:  # No batch norm en la última
                x = F.relu(x)
                x = self.bns[i](x)
                x = F.dropout(x, p=0.5, training=self.training)
        return F.log_softmax(x, dim=1)
```

### 4.5 Aplicación real: Red Eléctrica Española

```python
"""
Ejemplo aplicado: Modelar la red eléctrica española como grafo.

Nodos: subestaciones (con características de carga, generación)
Aristas: líneas de transmisión (con características de capacidad, distancia)
Tarea: predecir congestión / fallos en líneas
"""

import torch
from torch_geometric.nn import GCNConv, global_max_pool
from torch_geometric.data import Data

class PowerGridGNN(torch.nn.Module):
    """
    GNN para análisis de red eléctrica.
    
    Arquitectura:
    - Node features: [carga_actual, capacidad_generacion, tipo_subestacion, ...]
    - Edge features: [capacidad_linea, longitud, tipo_conductor, ...]
    - Output: probabilidad de congestión por línea
    """
    
    def __init__(self, node_feat_dim, edge_feat_dim, hidden_dim=64):
        super().__init__()
        
        # Proyectar features de nodos
        self.node_proj = torch.nn.Linear(node_feat_dim, hidden_dim)
        
        # Proyectar features de aristas
        self.edge_proj = torch.nn.Linear(edge_feat_dim, hidden_dim)
        
        # GCN layers con edge features (GatedGraphConv o GCNConv + edge MLP)
        self.conv1 = GCNConv(hidden_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        
        # Predictor de aristas (link prediction)
        self.edge_predictor = torch.nn.Sequential(
            torch.nn.Linear(hidden_dim * 2, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.3),
            torch.nn.Linear(hidden_dim, 1)  # probabilidad de congestión
        )
        
        # Predictor global (graph classification: estado de la red)
        self.graph_classifier = torch.nn.Sequential(
            torch.nn.Linear(hidden_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, 2)  # normal / congestión
        )
    
    def forward(self, x, edge_index, edge_attr, batch=None):
        """
        Args:
            x: (num_nodes, node_feat_dim)
            edge_index: (2, num_edges)
            edge_attr: (num_edges, edge_feat_dim)
            batch: (num_nodes,) - asignación nodo->grafo (para graph-level)
        """
        # Proyectar features
        h = F.relu(self.node_proj(x))
        e = F.relu(self.edge_proj(edge_attr))
        
        # Message passing
        h = F.relu(self.conv1(h, edge_index))
        h = F.dropout(h, p=0.3, training=self.training)
        h = F.relu(self.conv2(h, edge_index))
        
        # === Tarea 1: Link prediction (congestión por línea) ===
        # Para cada arista, concatenar embeddings de extremos
        src, dst = edge_index
        edge_embeddings = torch.cat([h[src], h[dst]], dim=1)
        edge_logits = self.edge_predictor(edge_embeddings)  # (num_edges, 1)
        
        # === Tarea 2: Graph-level classification ===
        if batch is not None:
            graph_embeddings = global_max_pool(h, batch)
            graph_logits = self.graph_classifier(graph_embeddings)
            return edge_logits, graph_logits
        
        return edge_logits


# === Simulación de datos de red eléctrica ===
def create_power_grid_simulation():
    """
    Crea un grafo simulado de una red eléctrica simplificada.
    """
    import numpy as np
    
    np.random.seed(42)
    
    # 50 subestaciones
    num_nodes = 50
    
    # Features de nodos: [carga_MW, capacidad_gen_MW, tipo (0=transformador, 1=subestacion), 
    #                     tension_kV (normalizada), demanda_pico_MW]
    node_features = torch.randn(num_nodes, 5)
    node_features[:, 2] = torch.randint(0, 2, (num_nodes,)).float()  # tipo
    
    # Aristas: líneas de transmisión (conectar nodos cercanos en "espacio")
    # Simulamos una topología tipo grid con conexiones extra
    edge_list = []
    for i in range(num_nodes):
        # Conectar con 3-5 vecinos más "cercanos"
        num_connections = np.random.randint(3, 6)
        targets = np.random.choice(
            [j for j in range(num_nodes) if j != i], 
            size=min(num_connections, num_nodes-1), 
            replace=False
        )
        for t in targets:
            edge_list.append([i, t])
    
    edge_list = torch.tensor(edge_list, dtype=torch.long).T
    
    # Features de aristas: [capacidad_MW, longitud_km (normalizada), 
    #                       tipo_conductor (0=AL, 1=ACSR, 2=AXL), pérdida_kW]
    num_edges = edge_list.shape[1]
    edge_attr = torch.randn(num_edges, 4)
    edge_attr[:, 2] = torch.randint(0, 3, (num_edges,)).float()
    
    # Labels: congestión por línea (binary)
    edge_labels = (torch.rand(num_edges) < 0.15).float()  # 15% congestión
    
    return (node_features, edge_list, edge_attr, edge_labels)

# Crear y entrenar
(x, edge_index, edge_attr, edge_labels) = create_power_grid_simulation()
model = PowerGridGNN(node_feat_dim=5, edge_feat_dim=4)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Training loop simplificado
for epoch in range(100):
    optimizer.zero_grad()
    edge_logits = model(x, edge_index, edge_attr)
    loss = F.binary_cross_entropy_with_logits(
        edge_logits.squeeze(), edge_labels
    )
    loss.backward()
    optimizer.step()
    if epoch % 25 == 0:
        print(f"Epoch {epoch}: loss = {loss.item():.4f}")
```

---

## 5. GNNs en la Práctica: Pitfalls y Soluciones

### 5.1 Over-smoothing

**Problema:** Con muchas capas (>5), los embeddings de nodos se vuelven idénticos.

**Soluciones:**
- Usar **residual connections** (skip connections entre capas)
- **DropEdge** (dropout en aristas durante training)
- **Graph Norm** / **Graph Layer Norm**
- Limitar a 2-3 capas y usar **aggregation global** para graph-level tasks

```python
class ResidualGCN(torch.nn.Module):
    """GCN con residual connections para combatir over-smoothing."""
    
    def __init__(self, num_features, num_classes, hidden_dim=64, num_layers=4):
        super().__init__()
        self.convs = torch.nn.ModuleList()
        self.residuals = torch.nn.ModuleList()
        
        self.convs.append(GCNConv(num_features, hidden_dim))
        for _ in range(num_layers - 1):
            self.convs.append(GCNConv(hidden_dim, hidden_dim))
            self.residuals.append(torch.nn.Linear(hidden_dim, hidden_dim))
        
        self.classifier = torch.nn.Linear(hidden_dim, num_classes)
    
    def forward(self, x, edge_index):
        for i, conv in enumerate(self.convs):
            h = conv(x, edge_index)
            h = F.relu(h)
            if i > 0:  # Residual desde la primera capa
                h = h + F.relu(self.residuals[i-1](x))
            x = h
        return self.classifier(x)
```

### 5.2 Escalabilidad

**Problema:** GCN requiere toda la matriz de adyacencia en memoria → O(n²).

**Soluciones:**
- **GraphSAGE:** muestreo de vecinos (k-hop)
- **ClusterGCN:** particionar grafo en clusters, batch training
- **GraphSAINT:** muestreo de subgrafos durante training
- **Neighbor sampling:** solo k vecinos por nodo

### 5.3 Heterogeneidad de Grafos

**Problema:** Múltiples tipos de nodos/aristas (ej: usuarios, productos, transacciones).

**Solución:** **Heterogeneous GNNs** con `torch_geometric.nn.HeteroConv`:

```python
from torch_geometric.nn import HeteroConv, SAGEConv

class HeteroGNN(torch.nn.Module):
    """GNN para grafos heterogéneos."""
    
    def __init__(self, metadata, hidden_dim=64):
        super().__init__()
        # metadata = ({node_type: num_features}, [(src_type, rel_type, dst_type)])
        self.convs = torch.nn.ModuleDict()
        
        for node_type in metadata[0]:
            self.convs[node_type] = SAGEConv(
                metadata[0][node_type], hidden_dim
            )
        
        # Conv heterogénea: aplica convs diferentes por tipo de arista
        self.hetero_conv = HeteroConv(
            {
                (src, rel, dst): SAGEConv(
                    metadata[0][src], hidden_dim
                )
                for src, rel, dst in metadata[1]
            },
            aggr='sum'
        )
        
        self.lin = torch.nn.Linear(hidden_dim, num_classes)
    
    def forward(self, x_dict, edge_index_dict):
        # x_dict: {node_type: tensor of features}
        # edge_index_dict: {(src, rel, dst): edge_index}
        x_dict = self.hetero_conv(x_dict, edge_index_dict)
        x_dict = {k: F.relu(v) for k, v in x_dict.items()}
        # Pool por tipo de nodo
        out = torch.cat([v.mean(dim=0) for v in x_dict.values()], dim=-1)
        return self.lin(out)
```

---

## 6. Aplicaciones al Stack ESIOS

### 6.1 Modelado de la Red Eléctrica Española

La red de transporte de REE es un grafo natural:

```
Nodos: ~200 subestaciones de alta tensión
Aristas: ~500 líneas de transmisión (220kV, 400kV)
Features nodo: carga, generación, tipo (transformador/subestación)
Features arista: capacidad, longitud, tipo conductor
Tareas:
  - Node classification: identificar subestaciones críticas
  - Link prediction: predecir congestión en líneas
  - Graph classification: estado global de la red (normal/crisis)
  - Temporal GNN: evolución horaria de la red
```

**Datos disponibles:**
- ESIOS: datos horarios de generación y demanda por zona
- REE: datos de red y flujos
- OpenStreetMap: topología de subestaciones

### 6.2 Integración con Series Temporales

Las GNNs + RNN/Transformer = **Spatio-Temporal GNNs**:

```python
"""
Spatio-Temporal GNN para predicción de demanda eléctrica.

- Espacial: GNN captura dependencias entre nodos de la red
- Temporal: GRU/LSTM captura evolución temporal
"""

class STGNN(torch.nn.Module):
    """Spatio-Temporal GNN para series temporales en grafos."""
    
    def __init__(self, num_nodes, num_features, hidden_dim=64, 
                 temporal_dim=32, num_layers=2):
        super().__init__()
        
        # Capa espacial: GCN captura dependencias topológicas
        self.gcn = GCNConv(num_features, hidden_dim)
        
        # Capa temporal: GRU captura evolución temporal
        self.gru = torch.nn.GRU(
            hidden_dim, temporal_dim, 
            num_layers=num_layers, batch_first=True
        )
        
        # Predictor
        self.fc = torch.nn.Linear(temporal_dim, 1)
    
    def forward(self, x, edge_index):
        """
        Args:
            x: (batch_size, seq_len, num_nodes, num_features)
            edge_index: (2, num_edges)
        Returns:
            predictions: (batch_size, seq_len, num_nodes, 1)
        """
        batch_size, seq_len, num_nodes, _ = x.shape
        
        # Para cada timestep, aplicar GCN
        gcn_outputs = []
        for t in range(seq_len):
            h = x[:, t, :, :]  # (batch, nodes, features)
            h = F.relu(self.gcn(h, edge_index))  # (batch, nodes, hidden)
            gcn_outputs.append(h)
        
        # (batch, seq_len, nodes, hidden) → (batch, seq_len, nodes, hidden)
        gcn_outputs = torch.stack(gcn_outputs, dim=1)
        
        # GRU por nodo
        predictions = []
        for node in range(num_nodes):
            node_seq = gcn_outputs[:, :, node, :]  # (batch, seq_len, hidden)
            _, h_n = self.gru(node_seq)  # (num_layers, batch, hidden)
            pred = self.fc(h_n[-1])  # (batch, 1)
            predictions.append(pred)
        
        return torch.stack(predictions, dim=2)  # (batch, 1, nodes, 1)
```

---

## 7. Papers Clave

| Paper | Año | Contribución |
|-------|-----|-------------|
| **Semi-Supervised Classification with GCNs** (Kipf & Welling) | 2017 | GCN original, convolución espectral aproximada |
| **Inductive Representation Learning on Large Graphs** (Hamilton et al.) | 2017 | GraphSAGE, muestreo de vecinos |
| **Graph Attention Networks** (Veličković et al.) | 2018 | Atención en grafos, multi-head |
| **Neural Message Passing for Quantum Chemistry** (Gilmer et al.) | 2017 | MPNN framework unificador |
| **How Powerful are Graph Neural Networks?** (Xu et al.) | 2019 | 1-WL test, GIN como límite expressivo |
| **Principal Neighbourhood Aggregation for Graph Nets** (Fei et al.) | 2020 | GIN, teoría de expressividad |
| **Graph Neural Networks: A Review of Methods and Applications** (Zhou et al.) | 2020 | Survey completa |
| **Spatio-Temporal Graph Neural Networks for Traffic Forecasting** (Yu et al.) | 2018 | STGCN, aplicación a tráfico |
| **BigCLAM: Scaling Graph Embeddings to Billions** (Sun et al.) | 2020 | Embeddings a escala web |
| **OGB: Open Graph Benchmark** (Hu et al.) | 2020 | Benchmark estándar para GNNs |

---

## 8. Repositorios de Referencia

| Repositorio | Descripción |
|-------------|-------------|
| [pyg-team/pytorch_geometric](https://github.com/pyg-team/pytorch_geometric) | **PyTorch Geometric** — Librería estándar para GNNs en PyTorch |
| [rusty1s/pytorch_scatter](https://github.com/rusty1s/pytorch_scatter) | Operaciones de scatter/gather para GNNs |
| [rusty1s/pytorch_sparse](https://github.com/rusty1s/pytorch_sparse) | Sparse tensors para grafos |
| [rusty1s/pytorch_cluster](https://github.com/rusty1s/pytorch_cluster) | Graph clustering (Spectral, Graclus) |
| [rusty1s/pytorch_spline_conv](https://github.com/rusty1s/pytorch_spline_conv) | Splines para convoluciones en grafos |
| [karpathy/llm.c](https://github.com/karpathy/llm.c) | No es GNN, pero útil para entender operaciones tensoriales básicas |

---

## 9. Conexión con Sesiones Anteriores

| Sesión previa | Conexión con GNNs |
|---------------|-------------------|
| **State Space Models** | Mamba puede operar sobre grafos (GraphMamba) |
| **Diffusion Models** | Diffusion sobre grafos para generación de moléculas |
| **Quantization** | GNNs cuantizados para edge deployment en MicroVM |
| **MoE** | MoE-GNNs para routing adaptativo en grafos grandes |

---

## 10. Tema Propuesto para la Siguiente Sesión

**FlashAttention** — Optimización de atención O(n²d) → O(n√d).

**Por qué:**
1. Es la optimización más importante en inference de transformers
2. Reduce memoria de O(n²d) a O(n√d) — crucial para MicroVM con 2GB RAM
3. Se usa en Llama.cpp, vLLM, y cualquier deployment de LLMs en edge
4. Complementa perfectamente la nota de quantización (ambas optimizan inference)
5. Implementación práctica en CUDA/Python con código real

**Alternativa:** Si FlashAttention ya está cubierto o no interesa → **LoRA / PEFT** (fine-tuning eficiente de LLMs, muy relevante para personalización del sistema).
