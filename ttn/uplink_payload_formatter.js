function readUint64BE(bytes, offset) {
  let value = 0;
  for (let i = 0; i < 8; i++) value = value * 256 + bytes[offset + i];
  return value;
}
function readInt32BE(bytes, offset) {
  let value = bytes[offset] * 0x1000000 + bytes[offset+1] * 0x10000 + bytes[offset+2] * 0x100 + bytes[offset+3];
  if (value >= 0x80000000) value -= 0x100000000;
  return value;
}
function readUint32BE(bytes, offset) {
  return bytes[offset] * 0x1000000 + bytes[offset+1] * 0x10000 + bytes[offset+2] * 0x100 + bytes[offset+3];
}
function readUint16BE(bytes, offset) { return bytes[offset] * 256 + bytes[offset+1]; }
function readInt16BE(bytes, offset) {
  let value = readUint16BE(bytes, offset);
  if (value >= 0x8000) value -= 0x10000;
  return value;
}
function decodeUplink(input) {
  const b = input.bytes;
  if (!b || b.length === 0) return { errors: ["Empty payload"] };
  if (b[0] === 1 && b.length >= 17) {
    return { data: {
      type: "login", id: readUint64BE(b,1),
      lon: readInt32BE(b,9) / 1000000,
      lat: readInt32BE(b,13) / 1000000,
      sensors: ["pm25","pm10","temperature","humidity","line_tracker","person_count","bicycle_count","car_count","batt"]
    }};
  }
  if (b[0] === 2 && b.length >= 26) {
    return { data: {
      type: "measure", id: readUint64BE(b,1), time: readUint32BE(b,9),
      readings: {
        pm25: readUint16BE(b,13)/10,
        pm10: readUint16BE(b,15)/10,
        temperature: readInt16BE(b,17)/10,
        humidity: readUint16BE(b,19)/10,
        line_tracker: b[21], person_count: b[22], bicycle_count: b[23], car_count: b[24], batt: b[25]
      }
    }};
  }
  return { errors: ["Unsupported payload type or invalid payload length"] };
}
