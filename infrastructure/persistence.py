import json
import sqlite3
import asyncio
from typing import Optional
from domain.entities import WorkflowCheckpoint, WorkflowState
from domain.repositories import CheckpointRepository

class SQLiteCheckpointRepository(CheckpointRepository):
    def __init__(self, db_path: str = "workflow_checkpoints.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS checkpoints (
                workflow_id TEXT PRIMARY KEY,
                current_step INTEGER,
                state TEXT,
                context_data TEXT,
                metadata TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    async def save(self, checkpoint: WorkflowCheckpoint) -> None:
        def _save():
            conn = sqlite3.connect(self.db_path)
            conn.execute("""
                INSERT OR REPLACE INTO checkpoints 
                (workflow_id, current_step, state, context_data, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                checkpoint.workflow_id,
                checkpoint.current_step,
                checkpoint.state.value,
                json.dumps(checkpoint.context_data),
                json.dumps(checkpoint.metadata)
            ))
            conn.commit()
            conn.close()
        
        await asyncio.get_event_loop().run_in_executor(None, _save)
    
    async def load(self, workflow_id: str) -> Optional[WorkflowCheckpoint]:
        def _load():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute(
                "SELECT * FROM checkpoints WHERE workflow_id = ?", 
                (workflow_id,)
            )
            row = cursor.fetchone()
            conn.close()
            return row
        
        row = await asyncio.get_event_loop().run_in_executor(None, _load)
        
        if row:
            return WorkflowCheckpoint(
                workflow_id=row[0],
                current_step=row[1],
                state=WorkflowState(row[2]),
                context_data=json.loads(row[3]),
                metadata=json.loads(row[4])
            )
        return None
    
    async def delete(self, workflow_id: str) -> None:
        def _delete():
            conn = sqlite3.connect(self.db_path)
            conn.execute("DELETE FROM checkpoints WHERE workflow_id = ?", (workflow_id,))
            conn.commit()
            conn.close()
        
        await asyncio.get_event_loop().run_in_executor(None, _delete)