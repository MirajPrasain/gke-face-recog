# Face Recognition Service

A stateless, horizontally scalable microservice for face detection, designed for the Bank-of-Anthos-inspired GKE microservice ecosystem.

## Overview

The Face Recognition Service provides standardized face detection capabilities through multiple interfaces:
- **HTTP/gRPC API** for synchronous requests
- **Model Context Protocol (MCP)** for AI agent integration
- **Event-driven architecture** for asynchronous processing

## Architecture Decision Record

**Status:** Proposed  
**Date:** 2025-09-20  
**Context:** Bank-of-Anthos-inspired GKE microservice ecosystem

### Decision

We introduce a new microservice `face-recognition-service` to provide face detection as a stateless, horizontally scalable service. It will be consumable both via synchronous HTTP/gRPC API and as a Model Context Protocol (MCP) tool (`detect_face`). Events will also be published asynchronously for other services (Email, Alert, Calendar).

### Motivation

- Current system lacks a vision intelligence module
- Teams need a standardized, production-ready interface for face recognition across different flows (security, KYC, productivity, alerts)
- AI agents should call the same logic via MCP without duplicating adapters
- Decoupling ensures scalability, cost control, and minimal blast radius if the model or infrastructure changes

## Interfaces

### 1. HTTP/gRPC API

#### Endpoint: `POST /detect_face`

**Request JSON:**
```json
{
  "image": {
    "url": "gs://bucket/image123.jpg",
    "bytes": "<base64-encoded>", 
    "options": {
      "model": "yolo-v8",
      "confidence": 0.7
    }
  }
}
```

**Response JSON:**
```json
{
  "detections": [
    {
      "bbox": [120, 55, 250, 200],
      "confidence": 0.91,
      "landmarks": {"eyes": [[130, 70], [190, 72]], "mouth": [160, 120]}
    }
  ],
  "latency_ms": 87,
  "request_id": "abc123"
}
```

#### Additional Endpoints

- `GET /healthz` – liveness probe
- `GET /readyz` – readiness probe  
- `GET /metrics` – Prometheus metrics

### 2. MCP Tool Contract

**Tool Name:** `detect_face`

**Description:** Detect faces in an image and return bounding boxes, confidence scores, and landmarks.

**Input Schema (JSON Schema draft-07):**
```json
{
  "type": "object",
  "properties": {
    "image_url": {"type": "string"},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
  },
  "required": ["image_url"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "detections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "bbox": {"type": "array", "items": {"type": "number"}},
          "confidence": {"type": "number"},
          "landmarks": {"type": "object"}
        },
        "required": ["bbox", "confidence"]
      }
    },
    "latency_ms": {"type": "integer"}
  },
  "required": ["detections"]
}
```

### 3. Event Schema (FaceEvent)

**Published to Pub/Sub topic:** `face-events`

```json
{
  "source": "face-recognition-service",
  "image_uri": "gs://bucket/image123.jpg",
  "detections": [
    {"bbox": [120, 55, 250, 200], "confidence": 0.91}
  ],
  "created_at": "2025-09-20T15:32:00Z",
  "correlation_id": "abc123"
}
```

## Service Level Objectives (SLOs)

- **Latency:** p95 < 200ms (CPU pool), p95 < 80ms (GPU pool)
- **Availability:** 99.9% monthly
- **Error budget:** ≤ 0.1% failed requests
- **Confidence threshold:** default 0.7, tunable per request

## Security & Access

- Service accessible only in-mesh via mTLS
- External calls routed through the Agent Orchestrator or API Gateway
- Workload Identity Federation used for GCS/Gmail API access
- RBAC + NetworkPolicies enforced at namespace level
- Binary Authorization ensures only signed/scanned images deploy

## Consequences

### Positive

- Other services (Email, Alert, Calendar) can subscribe without tight coupling
- AI agents can use MCP tool uniformly
- Horizontal Pod Autoscaler can scale based on CPU/GPU load
- Model upgrades (OpenCV → YOLO → new vision models) do not change the API/MCP contracts

### Considerations

- Additional infrastructure overhead for maintaining the service
- Need for proper monitoring and alerting for the face detection pipeline
- Model versioning strategy required for seamless updates

## Getting Started

### Prerequisites

- Kubernetes cluster with GKE
- Istio service mesh configured
- Pub/Sub topics created
- Workload Identity Federation setup

### Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n face-recognition
kubectl get services -n face-recognition
```

### Testing

```bash
# Test health endpoint
curl http://face-recognition-service/healthz

# Test face detection
curl -X POST http://face-recognition-service/detect_face \
  -H "Content-Type: application/json" \
  -d '{
    "image": {
      "url": "gs://your-bucket/test-image.jpg",
      "options": {
        "confidence": 0.8
      }
    }
  }'
```

## Monitoring

- Prometheus metrics available at `/metrics`
- Grafana dashboards for latency and error rates
- Alert rules configured for SLO violations
- Distributed tracing with Jaeger

## Contributing

1. Follow the established API contracts
2. Ensure backward compatibility
3. Update SLOs if performance characteristics change
4. Document any new model versions or configuration options

## License

[Add appropriate license information]

