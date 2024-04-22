export const jsonWithBigInt = (text) => {
    return JSON.parse(text, (key, value) => {
        if (typeof value === 'string' && (key === 'cid' || key === 'id')) {
          return BigInt(value);
        }
        return value;
    });
}

// export default { jsonWithBigInt };