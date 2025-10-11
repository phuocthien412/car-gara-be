# 🚀 Quy tắc làm việc theo nhóm với `GIT`

1. 💡 Trước khi `code` mới hoặc `push` code lên `github` thì cần phải kéo `code` mới nhất từ `github` về máy tính cá nhân - tránh bị xung đột `code` với câu lệnh

```bash
git pull origin master
```

2. 💡 Tạo nhánh mới để làm việc với từng `task` được giao:

```bash
git checkout -b ten-nhanh-moi
```

3. 💡 Khi đã kéo `code` từ `repo` nhánh `master` của dự án về thì trước khi push code cần phải tạo ra remote cá nhân của mình để tránh trường hợp không `push` được code lên remote của chủ dự án với câu lệnh

```bash
git remote add name_remote
```

- Với `name_remote` là tên remote mà bạn đặt

4. 💡 Khi có được các bước trên thì tiến hành đẩy code theo quy trình với lần lượt các câu lệnh sau:

```bash
git add .
git commit -m "[chatbox] name_commit day_commit version_commit"
git remote -v
git push -u name_remote name_branch
```

5. 💡 Sau khi đẩy code lên nhánh của mình thì đợi `Pull Request` từ người quản lý hoặc chủ ự án. Nếu họ xác nhận `Merge Request` thì tiến hành xóa nhánh cá nhân đã tạo với câu lệnh:

```bash
git branch -d <branch-name>
```

hoặc

```bash
git branch -D <branch-name>
```

6. 💡 Lưu ý nếu muốn tránh spam commit bằng câu lệnh sửa message commit gần nhất với câu lệnh:

```bash
git commit --amend -m "commit message"
```

7. 💡 Thêm file bị quên vào commit gần nhất bằng câu lệnh:

```bash
git add forgotten_file.py
git commit --amend --no-edit
```
