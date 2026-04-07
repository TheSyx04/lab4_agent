from langchain_core.tools import tool

# ==========================================================
# MOCK DATA - Du lieu gia lap he thong du lich
# Luu y: Gia ca co logic (VD: cuoi tuan dat hon, hang cao hon dat hon)
# ==========================================================

FLIGHTS_DB = {
	("Hà Nội", "Đà Nẵng"): [
		{
			"airline": "Vietnam Airlines",
			"departure": "06:00",
			"arrival": "07:20",
			"price": 1_450_000,
			"class": "economy",
		},
		{
			"airline": "Vietnam Airlines",
			"departure": "14:00",
			"arrival": "15:20",
			"price": 2_800_000,
			"class": "business",
		},
		{
			"airline": "VietJet Air",
			"departure": "08:30",
			"arrival": "09:50",
			"price": 890_000,
			"class": "economy",
		},
		{
			"airline": "Bamboo Airways",
			"departure": "11:00",
			"arrival": "12:20",
			"price": 1_200_000,
			"class": "economy",
		},
	],
	("Hà Nội", "Phú Quốc"): [
		{
			"airline": "Vietnam Airlines",
			"departure": "07:00",
			"arrival": "09:15",
			"price": 2_100_000,
			"class": "economy",
		},
		{
			"airline": "VietJet Air",
			"departure": "10:00",
			"arrival": "12:15",
			"price": 1_350_000,
			"class": "economy",
		},
		{
			"airline": "VietJet Air",
			"departure": "16:00",
			"arrival": "18:15",
			"price": 1_100_000,
			"class": "economy",
		},
	],
	("Hà Nội", "Hồ Chí Minh"): [
		{
			"airline": "Vietnam Airlines",
			"departure": "06:00",
			"arrival": "08:10",
			"price": 1_600_000,
			"class": "economy",
		},
		{
			"airline": "VietJet Air",
			"departure": "07:30",
			"arrival": "09:40",
			"price": 950_000,
			"class": "economy",
		},
		{
			"airline": "Bamboo Airways",
			"departure": "12:00",
			"arrival": "14:10",
			"price": 1_300_000,
			"class": "economy",
		},
		{
			"airline": "Vietnam Airlines",
			"departure": "18:00",
			"arrival": "20:10",
			"price": 3_200_000,
			"class": "business",
		},
	],
	("Hồ Chí Minh", "Đà Nẵng"): [
		{
			"airline": "Vietnam Airlines",
			"departure": "09:00",
			"arrival": "10:20",
			"price": 1_300_000,
			"class": "economy",
		},
		{
			"airline": "VietJet Air",
			"departure": "13:00",
			"arrival": "14:20",
			"price": 780_000,
			"class": "economy",
		},
	],
	("Hồ Chí Minh", "Phú Quốc"): [
		{
			"airline": "Vietnam Airlines",
			"departure": "08:00",
			"arrival": "09:00",
			"price": 1_100_000,
			"class": "economy",
		},
		{
			"airline": "VietJet Air",
			"departure": "15:00",
			"arrival": "16:00",
			"price": 650_000,
			"class": "economy",
		},
	],
}

HOTELS_DB = {
	"Đà Nẵng": [
		{
			"name": "Mường Thanh Luxury",
			"stars": 5,
			"price_per_night": 1_800_000,
			"area": "Mỹ Khê",
			"rating": 4.5,
		},
		{
			"name": "Sala Danang Beach",
			"stars": 4,
			"price_per_night": 1_200_000,
			"area": "Mỹ Khê",
			"rating": 4.3,
		},
		{
			"name": "Fivitel Danang",
			"stars": 3,
			"price_per_night": 650_000,
			"area": "Sơn Trà",
			"rating": 4.1,
		},
		{
			"name": "Memory Hostel",
			"stars": 2,
			"price_per_night": 250_000,
			"area": "Hải Châu",
			"rating": 4.6,
		},
		{
			"name": "Christina's Homestay",
			"stars": 2,
			"price_per_night": 350_000,
			"area": "An Thượng",
			"rating": 4.7,
		},
	],
	"Phú Quốc": [
		{
			"name": "Vinpearl Resort",
			"stars": 5,
			"price_per_night": 3_500_000,
			"area": "Bãi Dài",
			"rating": 4.4,
		},
		{
			"name": "Sol by Meliá",
			"stars": 4,
			"price_per_night": 1_500_000,
			"area": "Bãi Trường",
			"rating": 4.2,
		},
		{
			"name": "Lahana Resort",
			"stars": 3,
			"price_per_night": 800_000,
			"area": "Dương Đông",
			"rating": 4.0,
		},
		{
			"name": "9Station Hostel",
			"stars": 2,
			"price_per_night": 200_000,
			"area": "Dương Đông",
			"rating": 4.5,
		},
	],
	"Hồ Chí Minh": [
		{
			"name": "Rex Hotel",
			"stars": 5,
			"price_per_night": 2_800_000,
			"area": "Quận 1",
			"rating": 4.3,
		},
		{
			"name": "Liberty Central",
			"stars": 4,
			"price_per_night": 1_400_000,
			"area": "Quận 1",
			"rating": 4.1,
		},
		{
			"name": "Cochin Zen Hotel",
			"stars": 3,
			"price_per_night": 550_000,
			"area": "Quận 3",
			"rating": 4.4,
		},
		{
			"name": "The Common Room",
			"stars": 2,
			"price_per_night": 180_000,
			"area": "Quận 1",
			"rating": 4.6,
		},
	],
}


def _format_vnd(amount: int) -> str:
	return f"{amount:,}".replace(",", ".") + "đ"


@tool
def search_flights(origin: str, destination: str) -> str:
	"""
	Tim kiem cac chuyen bay giua hai thanh pho.

	Tham so:
	- origin: thanh pho khoi hanh (VD: 'Hà Nội', 'Hồ Chí Minh')
	- destination: thanh pho den (VD: 'Đà Nẵng', 'Phú Quốc')

	Tra ve danh sach chuyen bay voi hang, gio bay, gia ve.
	Neu khong tim thay tuyen bay, thu tra chieu nguoc.
	Neu chieu nguoc cung khong tim thay, tra ve thong bao khong co chuyen
	"""
	direct_key = (origin, destination)
	reverse_key = (destination, origin)

	flights = FLIGHTS_DB.get(direct_key)
	if flights:
		lines = [f"Tìm thấy {len(flights)} chuyến bay từ {origin} đến {destination}:"]
		for idx, flight in enumerate(flights, start=1):
			lines.append(
				f"{idx}. {flight['airline']} | {flight['departure']} - {flight['arrival']} | "
				f"{flight['class']} | {_format_vnd(flight['price'])}"
			)
		return "\n".join(lines)

	reverse_flights = FLIGHTS_DB.get(reverse_key)
	if reverse_flights:
		lines = [
			f"Không tìm thấy chuyến bay chiều {origin} -> {destination}.",
			f"Nhưng có {len(reverse_flights)} chuyến bay chiều ngược {destination} -> {origin}:",
		]
		for idx, flight in enumerate(reverse_flights, start=1):
			lines.append(
				f"{idx}. {flight['airline']} | {flight['departure']} - {flight['arrival']} | "
				f"{flight['class']} | {_format_vnd(flight['price'])}"
			)
		return "\n".join(lines)

	return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
	"""
	Tim kiem khach san tai mot thanh pho, co the loc theo gia toi da moi dem.

	Tham so:
	- city: ten thanh pho (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
	- max_price_per_night: gia toi da moi dem (VND), mac dinh khong gioi han

	Tra ve danh sach khach san phu hop voi ten, so sao, gia, khu vuc, rating.
	"""
	hotels = HOTELS_DB.get(city)
	if not hotels:
		available = ", ".join(HOTELS_DB.keys())
		return (
			f"Không có dữ liệu khách sạn cho {city}. "
			f"Bạn có thể thử: {available}."
		)

	filtered_hotels = [
		hotel for hotel in hotels if hotel["price_per_night"] <= max_price_per_night
	]
	filtered_hotels.sort(key=lambda item: item["rating"], reverse=True)

	if not filtered_hotels:
		return (
			f"Không tìm thấy khách sạn tại {city} với giá dưới "
			f"{_format_vnd(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."
		)

	lines = [
		f"Tìm thấy {len(filtered_hotels)} khách sạn tại {city} "
		f"(tối đa {_format_vnd(max_price_per_night)}/đêm):"
	]
	for idx, hotel in enumerate(filtered_hotels, start=1):
		stars = "★" * hotel["stars"]
		lines.append(
			f"{idx}. {hotel['name']} | {stars} | {_format_vnd(hotel['price_per_night'])}/đêm | "
			f"{hotel['area']} | rating {hotel['rating']}"
		)
	return "\n".join(lines)


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
	"""
	Tinh toan ngan sach con lai sau khi tru cac khoan chi phi.

	Tham so:
	- total_budget: tong ngan sach ban dau (VND)
	- expenses: chuoi mo ta cac khoan chi, moi khoan cach nhau boi dau phay
	  dinh dang 'ten_khoan:so_tien' (VD: 've_may_bay:890000,khach_san:650000')

	Tra ve bang chi tiet cac khoan chi va so tien con lai.
	Neu vuot ngan sach, canh bao ro rang so tien thieu.
	"""
	if total_budget < 0:
		return "Lỗi: total_budget phai la so nguyen khong am."

	if not expenses or not expenses.strip():
		return (
			"Lỗi: expenses đang rỗng. Đúng định dạng: "
			"'vé_bay:890000,khách_sạn:650000'."
		)

	parsed_expenses = {}
	for raw_item in expenses.split(","):
		item = raw_item.strip()
		if not item:
			continue

		if ":" not in item:
			return (
				f"Lỗi format tại mục '{item}'. "
				"Mỗi mục phải có dạng 'tên_khoản:số_tiền'."
			)

		name, amount_text = item.split(":", 1)
		name = name.strip()
		amount_text = amount_text.strip().replace(".", "")

		if not name:
			return "Lỗi: tên khoản chi không được để trống."
		if not amount_text.isdigit():
			return (
				f"Lỗi: số tiền '{amount_text}' của khoản '{name}' không hợp lệ. "
				"Vui lòng nhập số nguyên dương."
			)

		amount = int(amount_text)
		if amount < 0:
			return f"Lỗi: số tiền của khoản '{name}' không được âm."

		parsed_expenses[name] = parsed_expenses.get(name, 0) + amount

	if not parsed_expenses:
		return (
			"Lỗi: không đọc được khoản chi hợp lệ nào. "
			"Vui lòng kiểm tra lại chuỗi expenses."
		)

	total_expenses = sum(parsed_expenses.values())
	remaining = total_budget - total_expenses

	lines = ["Bảng chi phí:"]
	for name, amount in parsed_expenses.items():
		lines.append(f"- {name}: {_format_vnd(amount)}")
	lines.extend(
		[
			"---",
			f"Tổng chi: {_format_vnd(total_expenses)}",
			f"Ngân sách: {_format_vnd(total_budget)}",
			f"Còn lại: {_format_vnd(remaining)}",
		]
	)

	if remaining < 0:
		lines.append(f"Cảnh báo: Vượt ngân sách {_format_vnd(abs(remaining))}! Cần điều chỉnh.")

	return "\n".join(lines)


ALL_TOOLS = [search_flights, search_hotels, calculate_budget]
