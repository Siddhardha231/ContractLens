"""Multi-provider LLM client supporting Google Gemini Cloud, Ollama, and LM Studio."""
import httpx
from typing import Optional, Dict, Any
from app.config import (
    GEMINI_API_KEY,
    GEMINI_BASE_URL,
    OLLAMA_BASE_URL,
    LM_STUDIO_BASE_URL,
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
)
from app.extraction.prompts import EXTRACTION_SYSTEM_PROMPT, ASK_SYSTEM_PROMPT

class LLMClient:
    """Manages AI queries across Gemini, Ollama, and LM Studio."""

    @classmethod
    async def query_extraction(
        cls,
        prompt: str,
        model: str = DEFAULT_MODEL,
        provider: str = DEFAULT_PROVIDER,
        temperature: float = 0.1
    ) -> str:
        """Execute contract extraction against configured AI provider."""
        return await cls._query(
            system_prompt=EXTRACTION_SYSTEM_PROMPT,
            user_prompt=prompt,
            model=model,
            provider=provider,
            temperature=temperature,
            json_mode=True
        )

    @classmethod
    async def query_ask(
        cls,
        question: str,
        contract_text: str,
        model: str = DEFAULT_MODEL,
        provider: str = DEFAULT_PROVIDER,
        temperature: float = 0.1
    ) -> str:
        """Execute grounded Q&A query against configured AI provider."""
        user_prompt = f"""CONTRACT TEXT:
\"\"\"
{contract_text[:25000]}
\"\"\"

USER QUESTION: {question}

ANSWER (Concise, factual, with exact citations):"""

        return await cls._query(
            system_prompt=ASK_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            model=model,
            provider=provider,
            temperature=temperature,
            json_mode=False
        )

    @classmethod
    async def _query(
        cls,
        system_prompt: str,
        user_prompt: str,
        model: str,
        provider: str,
        temperature: float,
        json_mode: bool
    ) -> str:
        prov = provider.lower()
        if prov == "gemini" or "gemini" in model.lower():
            return await cls._query_gemini(system_prompt, user_prompt, model, temperature, json_mode)
        elif prov == "ollama":
            return await cls._query_ollama(system_prompt, user_prompt, model, temperature, json_mode)
        elif prov == "lmstudio":
            return await cls._query_lmstudio(system_prompt, user_prompt, model, temperature, json_mode)
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")

    @classmethod
    async def _query_gemini(
        cls,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        json_mode: bool
    ) -> str:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured in .env")

        model_name = model if "gemini" in model.lower() else "gemini-3.8-flash"
        url = f"{GEMINI_BASE_URL}/{model_name}:generateContent?key={GEMINI_API_KEY}"
        
        gen_config: Dict[str, Any] = {"temperature": temperature}
        if json_mode:
            gen_config["responseMimeType"] = "application/json"

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                url,
                json={
                    "system_instruction": {"parts": [{"text": system_prompt}]},
                    "contents": [{"parts": [{"text": user_prompt}]}],
                    "generationConfig": gen_config
                }
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                raise RuntimeError(f"Gemini API returned status {resp.status_code}: {resp.text}")

    @classmethod
    async def _query_ollama(
        cls,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        json_mode: bool
    ) -> str:
        payload: Dict[str, Any] = {
            "model": model,
            "prompt": user_prompt,
            "system": system_prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }
        if json_mode:
            payload["format"] = "json"

        async with httpx.AsyncClient(timeout=180.0) as client:
            resp = await client.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
            if resp.status_code == 200:
                return resp.json().get("response", "")
            else:
                raise RuntimeError(f"Ollama returned status {resp.status_code}: {resp.text}")

    @classmethod
    async def _query_lmstudio(
        cls,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        json_mode: bool
    ) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        async with httpx.AsyncClient(timeout=180.0) as client:
            resp = await client.post(f"{LM_STUDIO_BASE_URL}/chat/completions", json=payload)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            else:
                raise RuntimeError(f"LM Studio returned status {resp.status_code}: {resp.text}")
