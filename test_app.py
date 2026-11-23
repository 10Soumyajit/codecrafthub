import json
import tempfile
import unittest
from pathlib import Path

import app as app_module


class CodeCraftHubTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        app_module.DATA_FILE = Path(self.temp_dir.name) / "courses.json"
        app_module.app.config.update(TESTING=True)
        self.client = app_module.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def course_payload(self, **overrides):
        payload = {
            "name": "Python Basics",
            "description": "Learn Python fundamentals",
            "target_date": "2026-12-31",
            "status": "Not Started",
        }
        payload.update(overrides)
        return payload

    def test_frontend_is_served_and_uses_relative_api(self):
        with self.client.get("/") as response:
            self.assertEqual(response.status_code, 200)
            html = response.get_data(as_text=True)
        self.assertIn("CodeCraftHub", html)
        self.assertIn("const API_BASE = '/api/courses';", html)

    def test_create_and_get_course(self):
        response = self.client.post("/api/courses", json=self.course_payload())
        self.assertEqual(response.status_code, 201)
        course = response.get_json()
        self.assertEqual(course["id"], 1)
        self.assertIn("created_at", course)

        response = self.client.get("/api/courses")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [course])

    def test_validation_rejects_missing_fields_and_invalid_values(self):
        response = self.client.post("/api/courses", json={"name": "Incomplete"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", response.get_json()["error"])

        response = self.client.post(
            "/api/courses",
            json=self.course_payload(target_date="2026-02-30", status="Unknown"),
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/api/courses", data="not json")
        self.assertEqual(response.status_code, 400)

    def test_stats_endpoint_counts_all_statuses(self):
        for status in ("Not Started", "In Progress", "Completed"):
            response = self.client.post(
                "/api/courses",
                json=self.course_payload(name=status, status=status),
            )
            self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/courses/stats")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {
                "total_courses": 3,
                "courses_by_status": {
                    "Not Started": 1,
                    "In Progress": 1,
                    "Completed": 1,
                },
            },
        )

    def test_put_replaces_editable_fields_and_rejects_partial_update(self):
        create_response = self.client.post("/api/courses", json=self.course_payload())
        course_id = create_response.get_json()["id"]

        response = self.client.put(
            f"/api/courses/{course_id}",
            json=self.course_payload(name="Updated", status="Completed"),
        )
        self.assertEqual(response.status_code, 200)
        updated = response.get_json()
        self.assertEqual(updated["name"], "Updated")
        self.assertEqual(updated["status"], "Completed")

        response = self.client.put(
            f"/api/courses/{course_id}",
            json={"status": "In Progress"},
        )
        self.assertEqual(response.status_code, 400)

    def test_patch_updates_only_supplied_fields(self):
        create_response = self.client.post("/api/courses", json=self.course_payload())
        course_id = create_response.get_json()["id"]

        response = self.client.patch(
            f"/api/courses/{course_id}",
            json={"status": "In Progress"},
        )
        self.assertEqual(response.status_code, 200)
        updated = response.get_json()
        self.assertEqual(updated["status"], "In Progress")
        self.assertEqual(updated["name"], "Python Basics")

        response = self.client.patch(
            f"/api/courses/{course_id}",
            json={"status": "Unknown"},
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_and_missing_resources(self):
        create_response = self.client.post("/api/courses", json=self.course_payload())
        course_id = create_response.get_json()["id"]

        response = self.client.delete(f"/api/courses/{course_id}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.get_data(), b"")

        response = self.client.get(f"/api/courses/{course_id}")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

    def test_invalid_json_storage_file_returns_json_error(self):
        app_module.DATA_FILE.write_text("{invalid", encoding="utf-8")
        response = self.client.get("/api/courses")
        self.assertEqual(response.status_code, 500)
        self.assertIn("invalid JSON", response.get_json()["error"])

    def test_options_and_cors_headers(self):
        response = self.client.options("/api/courses")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.headers["Access-Control-Allow-Origin"], "*")

        response = self.client.get("/api/courses")
        self.assertEqual(response.headers["Access-Control-Allow-Origin"], "*")


if __name__ == "__main__":
    unittest.main()
