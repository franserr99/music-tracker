export type RenderItemFunction<T> = (item: T) => JSX.Element;
export interface GenericGridProps<T> {
  items: T[];
  renderItem: RenderItemFunction<T>;
}

export interface QuestionAnswer  {
  _id:string,
  answer:string

}
