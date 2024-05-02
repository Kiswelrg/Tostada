export const jsonWithBigInt = (input) => {
  const obj = typeof input === 'string' ? JSON.parse(input) : input;

  if (typeof obj !== 'object' || obj === null) {
    return obj; // Return the primitive value or null as it is
  }

  // Create a new object with the same properties as the original
  const newObj = Array.isArray(obj) ? [...obj] : { ...obj };

  // Recursively reset 'id' properties in nested objects
  for (const key in newObj) {
    if (newObj.hasOwnProperty(key)) {
      if (typeof newObj[key] === 'object') {
        newObj[key] = jsonWithBigInt(newObj[key]); // Recursively process nested objects
      } else if (key === 'cid' || key === 'id') {
        newObj[key] = BigInt(newObj[key]); // Set the 'id' property to 0
      }
    }
  }

  return newObj;
}

// export default { jsonWithBigInt };