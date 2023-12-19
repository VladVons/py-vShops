class TYield {
  *Generator1() {
    for (let i = 0; i < 10; i++) {
      yield i;
    }
  }

  *Generator2() {
    const values = ['one', 'two', 'three'];
    for (let i = 0; i < values.length; i++) {
      yield values[i];
    }
  }
}

const Yield = new TYield();

for (const x of Yield.Generator1()) {
  console.log(x);
}

for (const x of Yield.Generator2()) {
  console.log(x);
}
