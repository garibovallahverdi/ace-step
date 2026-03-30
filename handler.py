import runpod

def handler(job):
    prompt = job["input"].get("prompt", "Hello")

    return {
        "output": f"Model cavabı: {prompt}"
    }

runpod.serverless.start({
    "handler": handler
})
