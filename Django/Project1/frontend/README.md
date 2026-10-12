# Inkspot blog frontend

This Next.js app manages blog posts through the Django REST API.

## Run the app

In `Django/Project1/backend/blogconfig`, apply migrations and create a Django user:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

The post form requires the database ID of an existing Django user. Find it in the Django admin user-change URL, for example `/admin/auth/user/1/change/`.

Start Django from that same directory:

```powershell
python manage.py runserver
```

Then start the frontend in `Django/Project1/frontend`:

```powershell
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). By default, the frontend calls `http://localhost:8000/api/posts/`. To use a different Django origin, set `NEXT_PUBLIC_DJANGO_API_URL` before starting Next.js.

The API currently allows unauthenticated CRUD for local development. Add authentication and permissions before exposing it outside a trusted development environment.
