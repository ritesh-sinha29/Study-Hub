# =====================================================================
# RAG STUDY GUIDE: 03. KNOWLEDGE GRAPH RAG (NEO4J + CYPHER)
# =====================================================================
#
# INTRODUCTION & PURPOSE
# ----------------------
# Flat vector databases treat documents as a pile of unrelated text fragments. 
# While this is sufficient for basic lookups, it fails for complex reasoning 
# (e.g., "Find all components affected when API-01 is deprecated").
#
# Graph RAG builds structured Knowledge Graphs composed of Entities (Nodes) 
# and Relationships (Edges). This allows the retrieval engine to traverse the
# connections between entities to gather multi-hop facts.
#
# This script walks through the schema definition, entity extraction theory, 
# and the Cypher query logic used in advanced Graph RAG systems.
#
# =====================================================================
#                       THEORETICAL CORE CONCEPTS
# =====================================================================
#
# 1. THE ARCHITECTURE OF A KNOWLEDGE GRAPH
#    - Nodes (Entities): Representation of unique nouns (e.g. Person: "Harrison",
#      Company: "LangChain", Product: "LangGraph").
#    - Edges (Relationships): Named, directional connections linking nodes
#      (e.g., Harrison -[FOUNDED]-> LangChain).
#    - Properties: Key-value attributes stored on nodes or edges (e.g. `source_document`,
#      `timestamp`, `type`).
#
# 2. ENTITY & RELATIONSHIP EXTRACTION
#    - Standard pipelines use spaCy or fine-tuned NER (Named Entity Recognition)
#      models to extract entities.
#    - Production systems use LLMs with structured outputs to identify semantic triples:
#      `(Subject, Predicate/Relation, Object)`.
#
# 3. CYPHER QUERY LANGUAGE
#    - Cypher is the query language for Neo4j (similar to SQL for relational DBs).
#    - It uses ASCII-art style syntax to match patterns:
#      `MATCH (p:Person)-[:FOUNDED]->(c:Company) RETURN p.name, c.name`
#
# =====================================================================
#                     ARCHITECTURAL PIPELINE FLOW
# =====================================================================
#
#  [Raw Document] ──► LLM/NER Extractor ──► Semantic Triples ──► Cypher Ingest ──► [Neo4j DB]
#                                                                                    │
#  [User Query]   ──► Entity Resolver   ──► Cypher Query     ──► Subgraph Context ◄──┘
#
# =====================================================================

import os
from dotenv import load_dotenv

# Load credentials
load_dotenv()

# =====================================================================
# 1. CYPHER BLUEPRINTS
# =====================================================================

# Schema Constraint Blueprint:
# Enforces database level uniqueness on Entity names so we do not end up
# with multiple nodes representing the same entity (e.g. duplicating "Google").
INIT_CONSTRAINTS_CYPHER = """
CREATE CONSTRAINT unique_entity_name IF NOT EXISTS
FOR (e:Entity) REQUIRE e.name IS UNIQUE;
"""

# Graph Merge & Ingest Blueprint:
# Merges nodes (creates if missing, reads if already exists) and links them.
UPSERT_RELATIONSHIP_CYPHER = """
MERGE (s:Entity {name: $source_name})
ON CREATE SET s.type = $source_type

MERGE (t:Entity {name: $target_name})
ON CREATE SET t.type = $target_type

MERGE (s)-[r:RELATED {type: $relation_type}]->(t)
SET r.source_document = $doc_id
"""

# =====================================================================
# 2. EXTRACTION LOGIC
# =====================================================================

def extract_entities_and_relationships(text: str) -> dict:
    """
    Simulates Named Entity Recognition (NER) parsing text to extract
    structured entity relationships.
    """
    print("\n[Step 1] Parsing raw text for entities and relationships...")
    print(f"  Input Text: \"{text}\"")
    
    # Simulation of entity parsing:
    entities = [
        {"name": "LangGraph", "type": "FRAMEWORK"},
        {"name": "Harrison Chase", "type": "PERSON"},
        {"name": "LangChain", "type": "COMPANY"}
    ]
    
    relations = [
        {
            "source": "Harrison Chase", 
            "source_type": "PERSON", 
            "target": "LangChain", 
            "target_type": "COMPANY", 
            "relation_type": "FOUNDED"
        },
        {
            "source": "Harrison Chase", 
            "source_type": "PERSON", 
            "target": "LangGraph", 
            "target_type": "FRAMEWORK", 
            "relation_type": "CREATED"
        }
    ]
    
    return {"entities": entities, "relations": relations}


# =====================================================================
# 3. CONVERSION TO CYPHER INGEST STATEMENTS
# =====================================================================

def generate_ingest_statements(extracted_data: dict, document_id: str = "doc_001"):
    """
    Takes extracted JSON dictionaries and outputs standard Cypher ingestion queries.
    """
    print("\n[Step 2] Formatting extracted relationships into Cypher ingestion statements...")
    
    for idx, rel in enumerate(extracted_data["relations"], 1):
        # We replace variables in the Cypher string with concrete string literals
        cypher = (
            UPSERT_RELATIONSHIP_CYPHER
            .replace("$source_name", f"'{rel['source']}'")
            .replace("$source_type", f"'{rel['source_type']}'")
            .replace("$target_name", f"'{rel['target']}'")
            .replace("$target_type", f"'{rel['target_type']}'")
            .replace("$relation_type", f"'{rel['relation_type']}'")
            .replace("$doc_id", f"'{document_id}'")
        )
        
        print(f"\nRelationship #{idx} Ingestion query:")
        print(f"{'-'*40}")
        print(cypher.strip())
        print(f"{'-'*40}")


# =====================================================================
# EXECUTION ENTRY POINT
# =====================================================================

if __name__ == "__main__":
    print("="*70)
    print("KNOWLEDGE GRAPH RAG INGESTION BLUEPRINT STUDY")
    print("="*70)
    
    sample_corpus = "Harrison Chase founded LangChain and created LangGraph."
    
    # 1. Run extraction
    facts = extract_entities_and_relationships(sample_corpus)
    
    # 2. Display extracted JSON
    print("\nExtracted Entities JSON Schema:")
    for ent in facts["entities"]:
        print(f"  {ent}")
        
    print("\nExtracted Relationships JSON Schema:")
    for rel in facts["relations"]:
        print(f"  {rel}")
        
    # 3. Generate Ingest code
    generate_ingest_statements(facts)

# =====================================================================
# REAL-LIFE USE CASES
# =====================================================================
# 1. CYBERSECURITY THREAT INTELLIGENCE:
#    - Nodes: IP Addresses, Servers, User Accounts, File Hashes.
#    - Graph Traversals: If Server-A downloads File-X, and File-X has a hash linked to malware,
#      Graph RAG finds the malicious link instantly: `(Server)-[:DOWNLOADED]->(File)-[:HAS_HASH]->(Malware)`.
#
# 2. MEDICAL RECOMMENDATION ENGINES:
#    - Storing symptoms, diseases, medications, and clinical side effects. Allows query traversal:
#      `(Symptom) -[:INDICATES]-> (Disease) <-[:TREATS]- (Medication)`.

# =====================================================================
# MNC INTERVIEW PREPARATION
# =====================================================================
# Q1. What is the difference between Cypher's `CREATE` and `MERGE` statements?
# A:  - `CREATE` adds a node or relationship unconditionally. If run repeatedly, it duplicates data.
#     - `MERGE` acts as an "upsert". It searches for an existing pattern. If found, it reads/updates it.
#       If not found, it creates the node/relationship, preserving uniqueness constraints.
#
# Q2. How does Graph RAG solve the 'multi-hop reasoning' problem?
# A:  - Vector RAG cannot link disparate documents. For example, if Doc A says "A works at B" and Doc B 
#       says "B belongs to C", a vector query on "Where is A employed" might miss Doc B completely.
#     - Graph RAG represents these connections explicitly, allowing a Cypher traversal to hop across
#       nodes from A to B to C, returning the complete, connected answer.
