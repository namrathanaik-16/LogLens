from fastapi import APIRouter, UploadFile, File

from analyzers.error_detector import detect_errors, group_errors

router = APIRouter()


@router.post("/upload")
async def upload_log(file: UploadFile = File(...)):

    content = await file.read()

    text = content.decode("utf-8", errors="replace")

    lines = text.splitlines()

    errors = detect_errors(lines)

    grouped_errors = group_errors(errors)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "total_lines": len(lines),
        "total_errors": len(errors),
        "total_error_groups": len(grouped_errors),
        "errors": errors,
        "error_groups": grouped_errors
    }