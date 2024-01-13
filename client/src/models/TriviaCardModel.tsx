import mongoose from "mongoose";
export interface ITriviaCard extends Document {
    _id: string;
    answer: string;
}
const triviaCardSchema = new mongoose.Schema({
    _id:String, 
    answer:String
}, { collection: 'qna' });
const TriviaCardModel = mongoose.models.qna ||mongoose.model<ITriviaCard>('qna', triviaCardSchema);
export default TriviaCardModel;