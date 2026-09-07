from fastapi import APIRouter, UploadFile, File

from analyzers.error_detector import detect_errors, group_errors,generate_summary

router = APIRouter()


@router.post("/upload")
async def upload_log(file: UploadFile = File(...)):

    content = await file.read()

    text = content.decode("utf-8", errors="replace")

    lines = text.splitlines()

    errors = detect_errors(lines)

    grouped_errors = group_errors(errors)

    summary=generate_summary(grouped_errors)

    return{
        "filename":file.filename,
        "content_type":file.content_type,
        "summary":{
            "total_lines":len(lines),
            "total_errors":len(errors),
            "unique_issues":summary["unique_issues"]
        },
        "categories":summary["categories"],
        "top_issues":summary["top_issues"]
    }