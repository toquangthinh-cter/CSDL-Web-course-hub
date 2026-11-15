import test from "node:test";
import assert from "node:assert/strict";
import { api } from "../src/api.js";

test("GET trả về dữ liệu JSON khi thành công", async () => {
globalThis.fetch = async () => new Response(JSON.stringify([{ class_id: "WEB-01" }]), {
status: 200,
headers: { "Content-Type": "application/json" },
});
const data = await api("/sections");
assert.deepEqual(data, [{ class_id: "WEB-01" }]);
});

test("DELETE 204 trả về null", async () => {
globalThis.fetch = async () => new Response(null, { status: 204 });
const data = await api("/enrollments/22000004/WEB-01", { method: "DELETE" });
assert.equal(data, null);
});

test("Lỗi 404/409 ném Error kèm status và detail", async () => {
globalThis.fetch = async () => new Response(JSON.stringify({ detail: "Lop hoc phan da het cho" }), {
status: 409,
headers: { "Content-Type": "application/json" },
});
await assert.rejects(
() => api("/enrollments", { method: "POST", body: { student_id: "22000004", class_section_id: "WEB-01" } }),
(err) => err.status === 409 && err.message.includes("Lop hoc phan da het cho")
);
});

test("Lỗi 422 ghép mảng detail thành chuỗi thông báo", async () => {
globalThis.fetch = async () => new Response(JSON.stringify({ detail: [{ msg: "field required" }] }), {
status: 422,
headers: { "Content-Type": "application/json" },
});
await assert.rejects(() => api("/enrollments", { method: "POST", body: {} }), /field required/);
});

test("Lỗi mạng ném thông báo kiểm tra Backend/CORS", async () => {
globalThis.fetch = async () => { throw new TypeError("fetch failed"); };
await assert.rejects(() => api("/sections"), /Backend\/CORS/);
});